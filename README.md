1. Please share the formula being used for fitment criteria

- The formula depends upon the base weightage assigned in serviceline and some changes upon that before submitting the request.

fitment% = l*requestor_l + b*emp_ba + e*emp_e + r*emp_r
        + 0.6*t*emp_tskills + 0.4t*emp_tskills_proficiency
        + 0.6*f*emp_fskills + 0.4f*emp_fskills_proficiency
        + 0.6*e*emp_eskills + 0.4e*emp_eskills_proficiency

    Where,

    l = location
    b = bench ageing
    e = experience
    t = technical skills
    f = functional skills
    p = process skills
    r = rank

    emp_ba = Employee Bench-ageing metric.
    emp_e = Employee experience metric.
    emp_l = Employee location metric (contains location and alternate location).
    emp_tskills = technical skill branch mapped from skill tree as per demand.
    fmp_tskills = technical skill branch mapped from skill tree as per demand.
    emp_tskills = technical skill branch mapped from skill tree as per demand.



 2. How is proficiency being captured?
- If we are talking about skill proficiency here it is addressed while calculating the fitment %
as we can see in the formula also mentioned above.

 3. Is it AND or OR for skills - multiple combinations of skills should be satisfactory
- Currently it is OR for the skill matching if any of the skill is present in the skill_tree and the respected skill_branch OR skill is present in employee skills then fitment% will be assigned.

 4. Data is very minimal, there should a minimum of 50 records in the supply pool
- Sure.
 
 5. We observed fitment score going beyond 100, this needs to be corrected.
- Will be fixed.

 6. The i/p and o/p cannot be related once you submit, the i/p fields getting wiped off, better to have a reset button
- Will be Fixed.

 7. Sorting the search results will give us a better view
- Lack of communication.

 8. Sample data was provided for the purpose of understanding. Please mock up data as required.
- Will be fixed.


To Do :
-----------------
[high]Generate request and emp for diff scenarios, min 50 emps in supply pool

UI:
---
Proper serviceline weightage for the 1st time usage
update sliders to textbox and Add validation for sum = 100 (submit buttonshould be disabled).
add a reset button
show results in the same page.
Update the text for sort  All -> Sorted by Serviceline then %
Add a method to sort by just fitment %
[low]validation for Experience & Vacancies

Algo
----
if multiple skills are matched then select the one with max %.
Update the skill tree after the user selects the employees.
Optimise match_demand_skills() and reduce complexity. use time.time() for performance
Max skill level is assumed to 5


