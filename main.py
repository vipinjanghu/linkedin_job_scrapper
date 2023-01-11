from constant import url
from selenium import webdriver
from scr import linkedin
from flask import Flask, jsonify,request, render_template

from flask_cors import CORS,cross_origin
from selenium.webdriver.chrome.options import Options
#options = Options()
#options.add_argument("--headless")
#driver_path = r'chromedriver.exe'

app = Flask(__name__)

@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
@cross_origin()
def log():
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(driver_path)
    session_id = request.form['login_Id']
    password = request.form['password']
    lk = linkedin(driver,url)
    lk.login(session_id,password)
    return render_template('jobs.html')


@app.route('/search_jobs', methods=['POST'])
@cross_origin()
def job():
    driver_path = 'chromedriver.exe'
    driver = webdriver.Chrome(driver_path)
    search_job = request.form['content']
    lk = linkedin(driver,url)
    jo=lk.jobs(search_job)
    return render_template('try.html',job_list=jo)


if __name__=='__main__':
    app.run(debug=True,port=3000)