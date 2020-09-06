# Main file to find the matching employees as per demand.
# https://stackoverflow.com/questions/44458629/how-to-make-nested-for-loop-more-pythonic
import json 
from operator import itemgetter, attrgetter
import numpy as np
from gensim.models import KeyedVectors


related_skill_vectors = KeyedVectors.load("skillmodel.kv", mmap='r')


def mapping(demand):
    """
    Returns the sorted tuple of employees as per demand.

    Args:
        demand(dict): Dictionary which contains demand info.
    """
    serviceline_weightage = {
        "location_weight": int(demand.get("location_weight")),
        "experience_weight": int(demand.get("experience_weight")),
        "bench_weight": int(demand.get("bench_weight")),
        "rank_weight": int(demand.get("rank_weight")),
        "technical_weight": int(demand.get("technical_weight")),
        "functional_weight": int(demand.get("functional_weight")),
        "process_weight": int(demand.get("process_weight"))
    }
    emp_tuple_list = get_emp_wieghtage(demand, serviceline_weightage)

    items = sorted(emp_tuple_list, key=itemgetter(3, 2), reverse=True)
    sorted_by_fitment_percentage = sorted(emp_tuple_list, key=itemgetter(2), reverse=True)
    # items = sorted(emp_tuple_list, key=itemgetter(3, 2), reverse=True)
    for each in sorted_by_fitment_percentage:
        print(each[2])
    return items, sorted_by_fitment_percentage


def get_skill_kws(demand):
    """
    Filters the keywords from the demand dict for skill type.

    Args:
        demand(dict): Dictionary which contains demand info.
    """
    # try:
    technical_skill_kw, functional_skill_kw, process_skill_kw = [], [], []

    for i in range(1, 4):
        if demand.get("technical_skill_{}".format(i)):
            technical_skill_kw.append(''.join(demand.get("technical_skill_{}".format(i)).split(" ")))
    for i in range(1, 4):
        if demand.get("functional_skill_{}".format(i)):
            functional_skill_kw.append(''.join(demand.get("functional_skill_{}".format(i)).split(" ")))
    for i in range(1, 4):
        if demand.get("process_skill_{}".format(i)):
            process_skill_kw.append(''.join(demand.get("process_skill_{}".format(i)).split(" ")))

    return technical_skill_kw, functional_skill_kw, process_skill_kw
    # except AttributeError:
    #     pass

def calculate_serviceline_score(match_percentage, demand):
    """
    """
    for emp_id, each_item in match_percentage.items():
        if each_item["serviceline_info"]["service_line"] == demand["requestor_serviceline"].lower():
            each_item["serviceline_match"] += 1
            if each_item["serviceline_info"]["sub_service_line"] == demand["requestor_sub_serviceline"].lower():
                each_item["serviceline_match"] += 1
                if each_item["serviceline_info"]["smu"] == demand["requestor_smu"].lower(
                ):
                    each_item["serviceline_match"] += 1

    emp_tuple_list = []
    for emp_id, each_item in match_percentage.items():
        emp_tuple = (
            emp_id,
            each_item,
            match_percentage[emp_id]["fitment_percentage"],
            match_percentage[emp_id]["serviceline_match"])
        emp_tuple_list.append(emp_tuple)

    return emp_tuple_list


def get_skill_tuple(each_emp):
    """
    By observing the skill tree it looks like 
    unit1-unit3 are Technical skillls
    unit4-unit6 are Functional skillls
    unit7 is for the Process skills
    """
    emp_skill_tuple = {"technical": [], "functional": [], "process": []}
    for skill in each_emp.get("skills"):
        if skill["unit"] in ["unit_1", "unit_2", "unit_3"]:
            emp_skill_tuple["technical"].append((''.join(skill.get("skill","").split(" ")),skill.get("skill_level")))
        if skill["unit"] in ["unit_4", "unit_5", "unit_6"]:
            emp_skill_tuple["functional"].append((''.join(skill.get("skill","").split(" ")),skill.get("skill_level")))
        if skill["unit"] in "unit_7":
            emp_skill_tuple["process"].append((''.join(skill.get("skill","").split(" ")),skill.get("skill_level")))

    return emp_skill_tuple["technical"], emp_skill_tuple["functional"],emp_skill_tuple["process"]

def skill_match(request, available):
    try:
        if not request or not available:
            return 0
        available_skills,weightage_skills = [],[]
        for skill, weightage in available:
            available_skills.append(related_skill_vectors.get_vector(skill.lower().replace(" ","")))
            weightage_skills.append(int(weightage))

        available_skills = np.asarray(available_skills, dtype=np.float32)
        weightage_skills = np.asarray(weightage_skills, dtype=np.float32)
        requested_skill = np.array(related_skill_vectors.get_vector(request))
        weightage_skills = weightage_skills / 5.
        similarities = related_skill_vectors.cosine_similarities(requested_skill, available_skills)
        score = similarities * weightage_skills

        return max(score)
    except KeyError:
        return 0

def score_skill(request_skill, employee_skill, weight):

    skill_score = []
    if len(request_skill) < 1:
        skill_score.append(1)
    if len(request_skill) < 1:
        skill_score.append(0)
    else:
        for skill in request_skill:
            skill_score.append(skill_match(skill,employee_skill))
    skill_score = max(skill_score)
    employee_skill.append(skill_score*weight)
    return  employee_skill

def get_emp_wieghtage(demand, serviceline_weightage):
    """
    Calculates fitment % for each param present in serviceline weightage.
    Args:
        demand(dict): Dictionary which contains demand info.
    """
    supply_dict = json.load(open("new_supply.json", "r"))
    match_percentage = {}

    bench_age_list = [each.get("bench_ageing", 0)
                      for each in supply_dict.values()]
    max_rank = 5
    exp_list = [each.get("experience", 0)
                for each in supply_dict.values()]
    for emp_id,each_emp in supply_dict.items():    
        match_percentage[emp_id] = {
            "serviceline_info": {
                "service_line": each_emp.get("service_line"),
                "sub_service_line": each_emp.get("sub_service_line"),
                "smu": each_emp.get("smu")
            },
            "serviceline_weightage": {
                "experience": 0,
                "location": 0,
                "rank": 0,
                "bench_ageing": 0,
                "technical_skill": 0,
                "functional_skill": 0,
                "process_skill": 0
            },
            "fitment_percentage": 0,
            "serviceline_match": 0
        }  
        # Calculating % for experience
        match_percentage[emp_id]["serviceline_weightage"]["experience"] = (
            (each_emp.get("experience") - min(exp_list)) / (
                max(exp_list) - min(exp_list))) * serviceline_weightage.get(
            "experience_weight", 0)

        if each_emp.get("city").lower() in demand.get("location") or each_emp.get(
                "city").lower() in demand.get("alternate_location"):
            match_percentage[emp_id]["serviceline_weightage"]["location"] = serviceline_weightage.get(
                "location_weight", 0)

        # Calculating % for rank
        num = max_rank - abs(int(each_emp.get("rank",0)) - int(demand.get("rank",0)))
        match_percentage[emp_id]["serviceline_weightage"]["rank"] = (
            num / max_rank) * serviceline_weightage.get("rank_weight", 0)

        # Calculating % for bench ageing
        match_percentage[emp_id]["serviceline_weightage"]["bench_ageing"] = (
            (each_emp.get("bench_ageing") - min(bench_age_list)) / (
                max(bench_age_list) - min(bench_age_list))) * serviceline_weightage.get(
            "bench_weight", 0)

        # Calculating % for technical skills
        technical_skill_kw, functional_skill_kw, process_skill_kw = get_skill_kws(
            demand)

        technical_tuple, functional_tuple, process_tuple = get_skill_tuple(each_emp)

        technical_score = score_skill(technical_skill_kw, technical_tuple, serviceline_weightage.get("technical_weight"))
        functional_score = score_skill(functional_skill_kw, functional_tuple, serviceline_weightage.get("functional_weight"))
        process_score = score_skill(process_skill_kw, process_tuple, serviceline_weightage.get("process_weight"))

        match_percentage[emp_id]["serviceline_weightage"]["technical_skill"] = technical_score[-1]
        match_percentage[emp_id]["serviceline_weightage"]["functional_skill"] = functional_score[-1]
        match_percentage[emp_id]["serviceline_weightage"]["process_skill"] = process_score[-1]

        match_percentage[emp_id]["fitment_percentage"] = round(sum(
        match_percentage[emp_id]["serviceline_weightage"].values()),3)
    return calculate_serviceline_score(match_percentage, demand)

if __name__ == "__main__":
    
    demand = {
        "requestor_serviceline": "serviceline1",
        "requestor_sub_serviceline": "subserviceline3",
        "requestor_smu": "smu2",
        "job_title": "financial risk analyst",
        "rank": 3,
        "required_resources": 1,
        "country": "india",
        "location": "bangalore",
        "alternate_location": "",
        "technical_skill_1": "microsoft office",
        "technical_skill_2": "sdlc",
        "technical_skill_3": "",
        "functional_skill_1": "",
        "functional_skill_2": "risk analytics",
        "functional_skill_3": "accounting",
        "process_skill_1": "communication",
        "process_skill_2": "documentation",
        "process_skill_3": "team skill",
        "experience": 4,
        'location_weight': 30,
        'experience_weight': 10,
        'bench_weight': 0,
        'rank_weight': 10,
        'technical_weight': 10,
        'functional_weight': 30,
        'process_weight': 10
    }

    demand1 = {
        "requestor_serviceline": "serviceline2",
        "requestor_sub_serviceline": "subserviceline3",
        "requestor_smu": "smu1",
        "job_title": "Digital Marketing Expert",
        "rank": 4,
        "required_resources": 2,
        "country": "india",
        "location": "mumbai",
        "alternate_location": "",
        "technical_skill_1": "seo",
        "technical_skill_2": "googleadsense",
        "technical_skill_3": "",
        "functional_skill_1": "excel",
        "functional_skill_2": "",
        "functional_skill_3": "",
        "process_skill_1": "communication",
        "process_skill_2": "presentation skills",
        "process_skill_3": "",
        "experience": 2,
        'location_weight': 40,
        'experience_weight': 10,
        'bench_weight': 10,
        'rank_weight': 0,
        'technical_weight': 10,
        'functional_weight': 25,
        'process_weight': 5,
    }
    demand2 = {
        "requestor_serviceline": "serviceline3",
        "requestor_sub_serviceline": "subservicelin1",
        "requestor_smu": "smu3",
        "job_title": "UI developer",
        "rank": 3,
        "required_resources": 2,
        "country": "india",
        "location": "chennai",
        "alternate_location": "",
        "technical_skill_1": "vuejs",
        "technical_skill_2": "mongodb",
        "technical_skill_3": "",
        "functional_skill_1": "agile",
        "functional_skill_2": "sdlc",
        "functional_skill_3": "",
        "process_skill_1": "documentation",
        "process_skill_2": "presentation skills",
        "process_skill_3": "",
        "experience": 3,
        'location_weight': 40,
        'experience_weight': 20,
        'bench_weight': 30,
        'rank_weight': 0,
        'technical_weight': 15,
        'functional_weight': 20,
        'process_weight': 5
    }
    mapping(demand)