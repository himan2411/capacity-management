from flask import Flask, render_template, request, send_from_directory, request
from werkzeug.utils import secure_filename
import logging, os, json, traceback, random, subprocess, shutil
from get_mapped_employees import *
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
            print("---------------------------")
            print(emp_list)
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
            print(e)
    return render_template("form.html")
    
if __name__ == '__main__':
    app.run()