# linkedin_job_scrapper
Overall, this tool is useful for job seekers who want to automate the process of searching for jobs on LinkedIn and save the results for future reference.
This project is a web scraper that allows users to search for jobs on LinkedIn, and save the results in a database for later use. It utilizes the Python library Selenium to navigate the LinkedIn website  and to extract job information. The user can also log in to their LinkedIn account to access more job search results. The scraped data is stored in a MongoDB database, allowing users to retrieve the data at a later time without having to re-scrape the website. The application also provides a user-friendly web interface using Flask framework, which allows users to interact with the application through a web browser.

# Requirements :
- Flask==2.2.2
- requests==2.28.1
- Flask-Cors==3.0.10
- selenium==3.14.0
- pymongo==4.3.3

## Run:
- python app.py

## _WorkFlow of the Project_
![Workflow](https://user-images.githubusercontent.com/87582760/212266789-019f9b31-4364-4776-a6c7-33684dc0858c.png)

### Note:
The web scraper is limited to the number of jobs LinkedIn allows a user to scrape.
This project will scrape jobs upto two pages not more then that.
