import time

from constant import url
from selenium import webdriver
from scr import linkedin
from flask import Flask, jsonify,request, render_template

from flask_cors import CORS,cross_origin

app = Flask(__name__)
lk = linkedin(url)
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
@cross_origin()
def log():
    # driver_path = 'chromedriver.exe'
    # driver = webdriver.Chrome(driver_path)
    session_id = request.form['login_Id']
    password = request.form['password']
    #lk = linkedin(url)
    lk.login(session_id,password)
    check=lk.check_Credentials()
    if check == "Login Successfully":
        return render_template('job.html')
    else:
        return render_template('index1.html',error=check)


@app.route('/search_jobs', methods=['POST'])
@cross_origin()
def search_job():
    search_job = request.form['content']
    jo=lk.jobs(search_job)
    return render_template('results.html',job_list=jo)


@app.route('/want_another_job', methods=['POST'])
@cross_origin()
def want_another_job():
    i=request.form['content']
    lk.move_back(i)
    return render_template('job1.html')

@app.route('/another_job_search', methods=['POST'])
@cross_origin()
def another_job_search():
    search_job = request.form['content']
    jo = lk.jobs(search_job)
    return render_template('results.html', job_list=jo)

#
if __name__=='__main__':
    app.run(debug=True,port=70000)