# Main file to find the matching employees as per demand.

import json
from operator import itemgetter, attrgetter


def mapping(demand):
    """
    Returns the sorted tuple of employees as per demand.

    Args:
        demand(dict): Dictionary which contains demand info.
    """
    emp_tuple_list = get_emp_wieghtage(demand)

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
        open("skill_tree1.json",
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
    for branch_name, each_branch in skill_branches.items():
        for each_skill in each_branch:
            for each_emp_skill in each_emp_skills:
                if each_skill.get("unit") in each_emp_skill.get(
                        "primary_unit"):
                    if each_skill.get(
                            "sub_unit_1") in each_emp_skill.get("sub_unit_1"):
                        if each_skill.get(
                                "sub_unit_2") in each_emp_skill.get("sub_unit_2"):
                            if each_skill.get(
                                    "sub_unit_3") in each_emp_skill.get("sub_unit_3"):
                                if each_skill.get(
                                        "skill") in each_emp_skill.get("skill"):
                                    match_percentage[emp_id]["serviceline_weightage"]["{}_skill".format(branch_name)] = serviceline_weightage.get("{}_weight".format(
                                        branch_name)) * 0.6 + ((int(each_emp_skill["skill_level"]) - 1) / 4) * serviceline_weightage.get("{}_weight".format(branch_name)) * 0.4

    return match_percentage


def get_emp_wieghtage(demand):
    """
    Calculates fitment % for each param present in serviceline weightage.
    Args:
        demand(dict): Dictionary which contains demand info.
    """

    supply = open("supply.json", "r")
    supply_dict = json.load(supply)
    serviceline_weightage = {
        "location_weight": int(demand.get("location_weight")),
        "experience_weight": int(demand.get("experience_weight")),
        "bench_weight": int(demand.get("bench_weight")),
        "rank_weight": int(demand.get("rank_weight")),
        "technical_weight": int(demand.get("technical_weight")),
        "functional_weight": int(demand.get("functional_weight")),
        "process_weight": int(demand.get("process_weight"))
    }
    rank_list, exp_list, bench_age_list = [], [], []
    match_percentage = {}

    bench_age_list = [each.get("bench_ageing", 0)
                      for each in supply_dict.values()]
    rank_list = [int(each.get("rank", 0).lower().replace("rank_", ""))
                 for each in supply_dict.values()]
    exp_list = [each.get("years_of_experience", 0)
                for each in supply_dict.values()]

    for emp_id, each_emp in supply_dict.items():
        each_emp["id"] = emp_id.lower().replace(" ", "_")

        match_percentage[emp_id] = {
            "additional_credits": {},
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
            "fitment_percentage": 0
        }
        # Calculating % for experience
        match_percentage[emp_id]["serviceline_weightage"]["experience"] = (
            (each_emp.get("years_of_experience") - min(exp_list)) / (
                max(exp_list) - min(exp_list))) * serviceline_weightage.get(
            "experience_weight", 0)

        if each_emp.get("city").lower() in demand.get("location") or each_emp.get(
                "city").lower() in demand.get("alternate_location"):
            match_percentage[emp_id]["serviceline_weightage"]["location"] = serviceline_weightage.get(
                "location_weight", 0)

        # Calculating % for rank
        a = max(rank_list) - \
            int(each_emp.get("rank").lower().replace("rank_", ""))
        b = max(rank_list) - min(rank_list)
        match_percentage[emp_id]["serviceline_weightage"]["rank"] = (
            a / b) * serviceline_weightage.get("rank_weight", 0)

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
        with open("emp_fitment_percentage.json", "w") as f:
            f.write(json.dumps(match_percentage, indent="\t"))
        match_percentage[emp_id]["fitment_percentage"] = sum(
            match_percentage[emp_id]["serviceline_weightage"].values())

    for emp_id, each_item in match_percentage.items():
        each_item["serviceline_match"] = 0
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

    
if __name__ == "__main__":
    demand = {
    "requestor_serviceline": "serviceline1",
    "requestor_sub_serviceline": "subservicelin3",
    "requestor_smu": "smu2",
    "job_title": "financial risk analyst",
    "rank": "rank_3",
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
    "process_skill_1": "effective communication",
    "process_skill_2": "documentation",
    "process_skill_3": "team skill",
    "experience": 8,
    'location_weight': 30,
    'experience_weight': 10,
    'bench_weight': 0,
    'rank_weight': 10,
    'technical_weight': 10,
    'functional_weight': 30,
    'process_weight': 10
    }
    mapping(demand)                                                                                                                     