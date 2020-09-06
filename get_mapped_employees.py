# Main file to find the matching employees as per demand.
# https://stackoverflow.com/questions/44458629/how-to-make-nested-for-loop-more-pythonic
import json
from operator import itemgetter, attrgetter


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
    return items


def get_skill_kws(demand):
    """
    Filters the keywords from the demand dict for skill type.

    Args:
        demand(dict): Dictionary which contains demand info.
    """
    technical_skill_kw, functional_skill_kw, process_skill_kw = [], [], []

    for i in range(1, 4):
        technical_skill_kw.append(demand.get("technical_skill_{}".format(i)))
    for i in range(1, 4):
        functional_skill_kw.append(demand.get("functional_skill_{}".format(i)))
    for i in range(1, 4):
        process_skill_kw.append(demand.get("process_skill_{}".format(i)))

    return technical_skill_kw, functional_skill_kw, process_skill_kw


def get_skill_branches(
        job_title,
        technical_skill_kw,
        functional_skill_kw,
        process_skill_kw):
    """
    Returns the requested skill_branch for each skill type from demand.

    Args:
        job_title(string): Requested Job title.
        technical_skill_kw(list): keywords present in technical skill in demand.
        functional_skill_kw(list): keywords present in functional skill in demand.
        process_skill_kw(list): keywords present in process skill in demand.
    """
    skill_tree1 = json.load(
        open("new_tree.json",
            "r"))

    matched_skills = {"technical": [], "functional": [], "process": []}
    for skill in skill_tree1:
        for each_kw in technical_skill_kw:
            if each_kw in skill.values() and each_kw:
                matched_skills["technical"].append(skill)
        for each_kw in functional_skill_kw:
            if each_kw in skill.values() and each_kw:
                matched_skills["functional"].append(skill)
        for each_kw in process_skill_kw:
            if each_kw in skill.values() and each_kw:
                matched_skills["process"].append(skill)

    return matched_skills.get("technical"), matched_skills.get(
        "functional"), matched_skills.get("process")

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

def match_demand_skills(
        emp_id,
        each_emp_skills,
        skill_branches,
        match_dict,
        serviceline_weightage):
    """
    Assigns the match % by mapping skills from demand to each employee.

    Args:
        emp_id(string): Employee id
        each_emp_skills(dict): dict object of skills for each employee.
        skill_branches(dict): dict object of skill branches obtained from demand.
        match_dict(dict): dict onject of the calculated fitment %.
        serviceline_weightage(dict): dict object of the weightage obtained from demand.
    """
    match_percentage = match_dict
    for each_emp_skill in each_emp_skills:
        for branch_name, each_branch in skill_branches.items():
            for each_skill in each_branch:
                intersection_value = list(set(each_skill.values())& set(each_emp_skill.values()))
                if (each_emp_skill.get("skill") in intersection_value and each_emp_skill.get("skill")) or (each_emp_skill.get("sub_unit_3") in intersection_value and each_emp_skill.get("sub_unit_3")):
                    match_percentage[emp_id]["matched_skills"].append(each_emp_skill)
                    # Max skill level is considered 5.
                    weightage = serviceline_weightage.get("{}_weight".format(
                                            branch_name)) * 0.6 + ((int(each_emp_skill["skill_level"]) - 1) / 4) * serviceline_weightage.get("{}_weight".format(branch_name)) * 0.4
                    if weightage > match_percentage[emp_id]["serviceline_weightage"]["{}_skill".format(branch_name)]:
                        match_percentage[emp_id]["serviceline_weightage"]["{}_skill".format(branch_name)] = weightage
    
    # Removing duplicates from matched skills.
    match_percentage[emp_id]["matched_skills"] = [dict(t) for t in {tuple(d.items()) for d in match_percentage[emp_id].get("matched_skills")}]
    return match_percentage


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
    rank_list = [int(each.get("rank", 0))
                 for each in supply_dict.values()]
    exp_list = [each.get("experience", 0)
                for each in supply_dict.values()]
    for emp_id,each_emp in supply_dict.items():    
        match_percentage[emp_id] = {
            "serviceline_info": {
                "service_line": each_emp.get("service_line"),
                "sub_service_line": each_emp.get("sub_service_line"),
                "smu": each_emp.get("smu")
            },
            "matched_skills":[],
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
        num = max(rank_list) - \
            int(each_emp.get("rank",0))
        den = max(rank_list) - min(rank_list)
        match_percentage[emp_id]["serviceline_weightage"]["rank"] = (
            num / den) * serviceline_weightage.get("rank_weight", 0)

        # Calculating % for bench ageing
        match_percentage[emp_id]["serviceline_weightage"]["bench_ageing"] = (
            (each_emp.get("bench_ageing") - min(bench_age_list)) / (
                max(bench_age_list) - min(bench_age_list))) * serviceline_weightage.get(
            "bench_weight", 0)

        # Calculating % for technical skills
        technical_skill_kw, functional_skill_kw, process_skill_kw = get_skill_kws(
            demand)

        technical_skill_branch, functional_skill_branch, process_skill_branch = get_skill_branches(
            demand.get("job_title"), technical_skill_kw, functional_skill_kw, process_skill_kw)

        skill_branches = {
            "technical": technical_skill_branch,
            "functional": functional_skill_branch,
            "process": process_skill_branch
        }
        match_percentage = match_demand_skills(
            emp_id,
            each_emp["skills"],
            skill_branches,
            match_percentage,
            serviceline_weightage)
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
        "functional_skill_1": "risk analysis",
        "functional_skill_2": "analytics",
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
        "functional_skill_1": "advanced excel",
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