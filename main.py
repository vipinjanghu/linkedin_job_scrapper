from constant import url
from database import to_database, from_database
from constant import client, db
from scrapper import linkedin
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
import logging

logging.basicConfig(filename='app.log', level=logging.DEBUG)
app = Flask(__name__)
lk = linkedin(url)
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
@cross_origin()
def log():
    session_id = request.form['login_Id']
    password = request.form['password']
    lk.login(session_id, password)
    check = lk.check_Credentials()
    if check == "Login Successfully":
        return render_template('job.html')
    else:
        return render_template('index1.html', error=check)


@app.route('/search_jobs', methods=['POST'])
@cross_origin()
def search_job():
    source = request.form['source'].lower()
    search_job = request.form['content']
    job_name = search_job.replace(" ", "").lower()
    if source == "y":
        logging.info("Scrapping from linkedin")
        job_container = lk.jobs(search_job)
        logging.info("Scrapped Successfully")
        to_database(db, job_name, job_container)
        logging.info("Sent successfully to database")
        return render_template('results.html', job_list=job_container)
    elif source == "n":
        logging.info("Getting job from Database")
        job_container = from_database(db, job_name)
        if job_container == "Try again scrape via linkedin.":
            logging.info("Data not found on database")
            return render_template('job.html')
        else:
            logging.info("Successfully featched data from database")
            return render_template('results1.html', job_list=job_container)
    else:
        logging.error("Provide Right character Y/N only")
        return render_template('job1.html',error="Type Y/N only.")


@app.route('/want_another_job', methods=['POST'])
@cross_origin()
def want_another_job():
    i=request.form['content'].lower()
    if i=="y":
        logging.info("Looking for another job")
        lk.move_back(i)
        logging.info("Back on Home page")
        return render_template('job.html')
    elif i=="n":
        logging.info("Thanks for visiting ")
        return render_template('thanks.html')



if __name__=='__main__':
    app.run(debug=True)