# Main file to find the matching employees as per demand.

import json
from operator import itemgetter, attrgetter

def mapping(demands):
    # demands = open("demand.json", "r")
    # demand_dict = json.load(demands)
    print("----------in mapping-----------")
    print("----------demand-----------")
    print(demands)
    print("-------------------------------")
    emp_tuple_list = get_emp_wieghtage(demands)
    # getting weightage for 1st demand later calculate for every one

    items = sorted(emp_tuple_list, key=itemgetter(3, 2) ,reverse=True)
    
    
    
    return items

def get_skill_kws(demand):
    """
    Returns the keywords for each skill type.
    """
    technical_skill_kw, functional_skill_kw,process_skill_kw = [],[],[]
    
    technical_skill_kw.append(demand.get("technical_skill_1"))
    technical_skill_kw.append(demand.get("technical_skill_2"))
    technical_skill_kw.append(demand.get("technical_skill_3"))
    functional_skill_kw.append(demand.get("functional_skill_1"))
    functional_skill_kw.append(demand.get("functional_skill_2"))
    functional_skill_kw.append(demand.get("functional_skill_3"))
    process_skill_kw.append(demand.get("process_skill_1"))
    process_skill_kw.append(demand.get("process_skill_2"))
    process_skill_kw.append(demand.get("process_skill_3"))
    
    return technical_skill_kw, functional_skill_kw, process_skill_kw

def get_skill_branches(job_title, technical_skill_kw, functional_skill_kw,process_skill_kw):
    """
    returns the matched skill branch from the skill_tree by matching keywords.
    """
    # skill_tree = json.load(open("skill_tree.json", "r"))
    skill_tree1 = json.load(open("/home/harsh/Desktop/capacity_management/flask_app/skill_tree1.json", "r"))

    matched_skills = {"technical":[],"functional":[],"process":[]}
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
    
    return matched_skills.get("technical"), matched_skills.get("functional"), matched_skills.get("process")
        

        
        # if each not in skill_tree:
        #     for each_unit in skill_tree:
        #         if each not in skill_tree[each_unit]:
        #             for each_sub_unit in skill_tree[each_unit].keys():
        #                 if each 

def match_demand_skills(emp_id, each_emp_skills, skill_branches, match_dict, serviceline_weightage):
    match_percentage = match_dict
    for branch_name,each_branch in skill_branches.items():
        for each_skill in each_branch:
            for each_emp_skill in each_emp_skills:
                if each_skill.get("unit") in each_emp_skill.get("primary_unit"):
                    if each_skill.get("sub_unit_1") in each_emp_skill.get("sub_unit_1"):
                        if each_skill.get("sub_unit_2") in each_emp_skill.get("sub_unit_2"):
                            if each_skill.get("sub_unit_3") in each_emp_skill.get("sub_unit_3"):
                                if each_skill.get("skill") in each_emp_skill.get("skill"):
                                    match_percentage[emp_id]["serviceline_weightage"]["{}_skill".format(branch_name)] = serviceline_weightage.get("{}_weight".format(branch_name))*0.6 + int(each_emp_skill["skill_level"])*0.4
                                    # if not match_percentage[emp_id]["additional_credits"].get("{}_skill_value".format(branch_name)):
                                    #     match_percentage[emp_id]["additional_credits"]["{}_skill_value".format(branch_name)] = int(int(each_emp_skill["skill_level"])*(serviceline_weightage["skill"].get(branch_name)/10))
                                    # else:
                                    #     match_percentage[emp_id]["additional_credits"]["{}_skill_value".format(branch_name)] += int(int(each_emp_skill["skill_level"])*(serviceline_weightage["skill"].get(branch_name)/10))

    return match_percentage

def get_emp_wieghtage(demand):
    
    supply = open("/home/harsh/Desktop/capacity_management/flask_app/supply.json", "r")
    supply_dict = json.load(supply)

    # service_line = demand.get("requestor_serviceline")
    # serviceline_weightage = json.load(open("serviceline_rules.json", "r"))["weightage"].get(service_line.lower())
    serviceline_weightage = {
        "location_weight": int(demand.get("location_weight")),
        "experience_weight": int(demand.get("experience_weight")),
        "bench_weight": int(demand.get("bench_weight")),
        "rank_weight": int(demand.get("rank_weight")),
        "technical_weight": int(demand.get("technical_weight")),
        "functional_weight": int(demand.get("functional_weight")),
        "process_weight": int(demand.get("process_weight"))
    }
    rank_list, exp_list, bench_age_list = [],[],[]
    match_percentage = {}
    
    bench_age_list = [each.get("bench_ageing",0) for each in supply_dict.values()]
    rank_list = [int(each.get("rank",0).lower().replace("rank_","")) for each in supply_dict.values()]
    exp_list = [each.get("years_of_experience",0) for each in supply_dict.values()]
   


    for emp_id,each_emp in supply_dict.items():
        each_emp["id"] = emp_id.lower().replace(" ", "_")
        
        match_percentage[emp_id] = {
            "additional_credits":{},
            "serviceline_info":{
                "service_line":each_emp.get("service_line"),
                "sub_service_line":each_emp.get("sub_service_line"),
                "smu":each_emp.get("smu")
            },
            "serviceline_weightage":{
                "experience":0,
                "location":0,
                "rank":0,
                "bench_ageing":0,
                "technical_skill":0,
                "functional_skill":0,
                "process_skill":0
            },
            "fitment_percentage":0
        }
        # Calculating % for experience
        match_percentage[emp_id]["additional_credits"]["experience"] = ((each_emp.get("years_of_experience")-min(exp_list))/(max(exp_list)-min(exp_list)))*serviceline_weightage.get("experience_weight",0)
        
        # match_percentage[emp_id]["experience_value"] = each_emp.get("years_of_experience")
        # if each_emp.get("years_of_experience") >= demand.get("experience"):
        #     match_percentage[emp_id]["serviceline_weightage"]["experience"] = serviceline_weightage.get("experience",0)*0.6 + each_emp.get("years_of_experience",0)*0.4
        #     # match_percentage[emp_id]["additional_credits"]["experience"] = each_emp.get("years_of_experience",0) - demand.get("experience",0)
        # else:
        #     match_percentage[emp_id]["serviceline_weightage"]["experience"] = (int(each_emp.get("years_of_experience"))/int(demand.get("experience")))*serviceline_weightage.get("experience",0)

        # Calculating % for location
        # include scenarios for alternate location
        # match_percentage[emp_id]["location_value"] = demand.get("location")
        # match_percentage[emp_id]["alternate_location"] = demand.get("alternate_location")
        if each_emp.get("city").lower() in demand.get("location") or each_emp.get("city").lower() in demand.get("alternate_location"):
            match_percentage[emp_id]["serviceline_weightage"]["location"] = serviceline_weightage.get("location_weight",0)
        
        
        # Calculating % for rank
        # including rank value for further comparition
        match_percentage[emp_id]["serviceline_weightage"]["rank"] = (( int(each_emp.get("rank").lower().replace("rank_",""))-min(rank_list))/(max(rank_list)-min(rank_list)))*serviceline_weightage.get("rank_weight",0)

        # match_percentage[emp_id]["rank_value"] = int(each_emp.get("rank").lower().replace("rank_",""))
        # if int(each_emp.get("rank").lower().replace("rank_","")) <= int(demand.get("rank").lower().replace("rank_","")):
        #     match_percentage[emp_id]["serviceline_weightage"]["rank"] = serviceline_weightage.get("rank",0)*0.6
        #     rank_diff = int(demand.get("rank").lower().replace("rank_","")) - int(each_emp.get("rank").lower().replace("rank_",""))
            # match_percentage[emp_id]["additional_credits"]["rank"] = rank_diff
            # match_percentage[emp_id]["serviceline_weightage"]["rank"] += 0.4*rank_diff
            # here rank1 should get more priority than rank2 if demand is of rank3
        # else:
        #     match_percentage[emp_id]["serviceline_weightage"]["rank"] = int(((5 - int(each_emp.get("rank").lower().replace("rank_","")))/5)*serviceline_weightage.get("rank",0))

        # Calculating % for bench ageing
        match_percentage[emp_id]["serviceline_weightage"]["bench_ageing"] = ((each_emp.get("years_of_experience")-min(bench_age_list))/(max(bench_age_list)-min(bench_age_list)))*serviceline_weightage.get("bench_weight",0)

        # if int(each_emp.get("bench_ageing")) > 0:
        #     match_percentage[emp_id]["serviceline_weightage"]["bench_ageing"] = serviceline_weightage.get("bench_ageing",0)
        #     match_percentage[emp_id]["additional_credits"]["bench_ageing_value"] = int(each_emp.get("bench_ageing"))

        # Calculating % for technical skills
        # create a list of skill keywords for matching.
        technical_skill_kw, functional_skill_kw, process_skill_kw = get_skill_kws(demand)

        technical_skill_branch, functional_skill_branch, process_skill_branch = get_skill_branches(demand.get("job_title"), technical_skill_kw, functional_skill_kw, process_skill_kw)

        skill_branches = {
            "technical": technical_skill_branch,
            "functional":functional_skill_branch,
            "process":process_skill_branch
        }
        match_percentage = match_demand_skills(emp_id, each_emp["skills"], skill_branches, match_percentage, serviceline_weightage)
        with open("emp_fitment_percentage.json", "w") as f:
            f.write(json.dumps(match_percentage, indent="\t"))
        match_percentage[emp_id]["fitment_percentage"] = sum(match_percentage[emp_id]["serviceline_weightage"].values())

    for emp_id,each_item in match_percentage.items():
        each_item["serviceline_match"] = 0
        if each_item["serviceline_info"]["service_line"] == demand["requestor_serviceline"].lower():
            each_item["serviceline_match"] += 1
            if each_item["serviceline_info"]["sub_service_line"] == demand["requestor_sub_serviceline"].lower():
                each_item["serviceline_match"] += 1
                if each_item["serviceline_info"]["smu"] == demand["requestor_smu"].lower():
                    each_item["serviceline_match"] += 1
    
    emp_tuple_list = []
    for emp_id,each_item in match_percentage.items():
        emp_tuple = (emp_id,each_item, match_percentage[emp_id]["fitment_percentage"], match_percentage[emp_id]["serviceline_match"])
        emp_tuple_list.append(emp_tuple)
    
    return emp_tuple_list
    
                            
# if __name__ == "__main__":
#     demands = {'requestor_serviceline': 'ServiceLine1', 'requestor_sub_serviceline': 'SubServiceLine1', 'requestor_smu': 'SMU1', 'job_title': 'a', 'functional_skill_1': 'sadsada', 'functional_skill_2': 'dsffsd', 'functional_skill_3': 'sdf', 'techincal_skill_1': 'erwj', 'techincal_skill_2': 'njdsfksjk', 'techincal_skill_3': 'dmdnfs', 'process_skill_1': 'ndskjfn', 'process_skill_2': 'dns', 'process_skill_3': 'v', 'country': 'ndfskjn', 'location': 'dnsdkjjf', 'alternate_location': 'dnsdkjkf', 'experience': 'sdksnskjf', 'rank': 'jh', 'required_resources': 'kdndfkjsdj', 'location_weight': 20, 'experience_weight': 20, 'bench_weight': 50, 'rank_weight': 50, 'technical_weight': 50, 'dunctional_weight': 50, 'process_weight': 50}
#     main([demands])
