from flask import Flask, render_template, request, send_from_directory, request
from werkzeug.utils import secure_filename
import logging, os, json, traceback, random, subprocess, shutil
from get_mapped_employees import *
import random
import pandas as pd
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template("form.html")

@app.route('/supply', methods = ['POST'])
def supply():
    if request.method == 'POST':
        try:
            form = request.form.to_dict()
            print(form)
            emp_list = mapping(form)
            fitment_score = {}
            #load supply chart
            supply = open("supply.json", "r")
            supply_dict = json.load(supply)
            #create dictionary with id and fitment score
            for item in emp_list:
                fitment_score[item[0]] = item[2]
            #traverse over fitment dictionary to get other parameters
            print(fitment_score.keys())
            data = []
            for emp_id in fitment_score.keys():
                row = {}
                row['e_id'] = emp_id
                row['fitment'] = round(fitment_score[emp_id],2)
                row['smu_info'] = supply_dict[emp_id]["service_line"] + "->" + supply_dict[emp_id]["sub_service_line"] + "->" + supply_dict[emp_id]["smu"]
                row['skills'] = [i['skill'] for i in supply_dict[emp_id]["skills"]]
                row['experience'] = supply_dict[emp_id]["experience"]
                row['rank'] = supply_dict[emp_id]["rank"]
                row['location'] = supply_dict[emp_id]["city"]
                row['bench'] = supply_dict[emp_id]["bench_ageing"]
                data.append(row)
            
            print(data)
            with open("response.txt", "a") as resp:
                resp.write("# Demand\n")
                resp.write(json.dumps(form))
                resp.write("\n\nResults\n{}\n".format("-"*95))
                resp.write("empid \t\t fitment% \t\t serviceline \t\t sub_service_line \t smu\n")
                resp.write("{}\n".format("-"*95))
                for each_item in emp_list:
                    resp.write("{} \t\t {} \t\t {} \t\t {} \t {}\n".format(each_item[0], each_item[2], each_item[1]["serviceline_info"]["service_line"],each_item[1]["serviceline_info"]["sub_service_line"],each_item[1]["serviceline_info"]["smu"]))
                resp.write(emp_list)
        except Exception as e:
            emp_list = mapping(form)
            print(e)
    return render_template("form.html", data=data , request=form, form=form)
    
@app.route('/forward', methods = ['POST'])
def forward():
    if request.method == 'POST':
        existing_table = pd.read_csv("item_item.csv")
        form = request.form.to_dict()
        req_id = random.randint(1,100000)
        ratings_dict = { "request": [req_id]* (len(form.keys())-2),
        "item": [i for i in form.keys()][:-2]
        }
        new_df = pd.DataFrame(ratings_dict)
        existing_table = existing_table.append(new_df)  
        print(existing_table)  
        existing_table.to_csv("item_item.csv",index=False,header=True)
        print([i for i in form.keys()][:-1])
    return render_template("index.html",data= " ".join([i for i in form.keys()][:-1]))

if __name__ == '__main__':
    app.run()