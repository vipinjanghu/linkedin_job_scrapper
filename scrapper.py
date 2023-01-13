from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import logging

logging.basicConfig(filename='app.log', level=logging.INFO)



class linkedin():
    '''url:is the link of Linkedin login page
      driver:

    '''
    driver_path = 'chromedriver.exe'
    # options = Options()
    #
    # options.add_argument("--headless")
    def __init__(self, url, driver=webdriver.Chrome(driver_path)):
        self.driver = driver
        self.url = url
        # self.login_id=login_id
        # self.login_password=login_password
        # self.job_name=job_name

    def login(self, login_id, login_password):
        '''
         return:This function will send our user_id and password to lindkin to login.
         login_id:user id of linkedin
         password:of linkedin account
        '''
        try:
            self.driver.get(self.url)
            # Wait for the "session_key" element to be clickable before interacting with it
            user_id = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "session_key"))
            )
            user_id.send_keys(login_id)
            # Wait for the "session_password" element to be clickable before interacting with it
            passw = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.ID, "session_password"))
            )
            passw.send_keys(login_password)

            # Wait for the "sign-in-form__submit-button" element to be clickable before interacting with it
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "sign-in-form__submit-button"))
            ).click()

        except TimeoutError as e:
            logging.error("Timeout Error: Failed to load page or find login elements")
        except Exception as e:
            logging.error("An unexpected error occurred: ", e)


    def check_Credentials(self):
        ''' This function will return if we have wrong user_id or wrong password'''
        try:
            if WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "form__input--error"))).get_attribute(
                    "id") == "username":
                logging.error("Wrong user id provided")
                return str("Wrong User Id")
            elif WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "form__input--error"))).get_attribute(
                    "id") == "password":
                logging.error("Wrong password")
                return str("Wrong Password")
        except:
            logging.info("Login Successfully")
            return str("Login Successfully")

    def search_filter(self, job_name):
        '''
            This function will filter our search results based on time of post and on most recent
            job_name:string of job which we want to scrape
        '''
        #Wait for the "search-global-typeahead__input" element to be clickable before interacting with it
        try:
            search = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "search-global-typeahead__input"))
            )

            search.send_keys(job_name)
            search.send_keys(Keys.ENTER)
            logging.info("Successfully Sent the Job name to search bar.")
        except Exception as e:
            logging.exception("Not able to find the search bar.")

        # Wait for the "All filters" element to be clickable before interacting with it
        try:
            all_filter = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//*[text()='All filters']"))
            )
            all_filter.click()

            # Wait for the "advanced-filter-sortBy-DD" element to be clickable before interacting with it
            ab = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "search-reusables__value-label"))
            )
            time.sleep(1)
            for i in ab:
                if i.get_attribute("for") == "advanced-filter-sortBy-DD":  # most recent filter
                    i.click()
                if i.get_attribute("for") == "advanced-filter-timePostedRange-r86400":  # Past 24 hour filter
                    i.click()

            # Wait for the show result button to be clickable before interacting with it
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/div/div[3]/div/button[2]'))
            ).click()
            logging.info("Successfully applied the filter")
        except Exception as e:
            logging.debug("Not able to apply filter ")
        self.driver.maximize_window()
        time.sleep(1)

    def scroll(self):
        '''
             It will scroll our inner scrollbar attached with a scrable element
        '''
        try:
            ele = self.driver.find_element_by_xpath('//*[@id="main"]/div/section[1]/div')
            self.driver.execute_script("arguments[0].scroll(0, arguments[0].scrollHeight);", ele)
            logging.info("Successfully scrolled the page")
        except Exception as e:
            logging.exception(e)

        time.sleep(1)

    def pages(self):
        '''
            It will featch the page no which containg jobs

        '''
        try:
            pg_2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'li[data-test-pagination-page-btn="2"]'))
            )
            logging.info("Successfully find the 2nd page.")
            return pg_2
        except:
            logging.info("2nd page not available")


    def job_cont(self):
        '''
            It will featch all element that containg the jobs
        '''

        job_container = WebDriverWait(self.driver, 10).until(
            lambda driver: self.driver.find_element_by_class_name("scaffold-layout__list-container"))

        # Now you can find the elements using the xpath

        jo = job_container.find_elements_by_xpath(".//li/div/div[1]")
        return jo

    def job_detail(self):
        '''
        This function will scrap all the deatils related to a job posted on linkedin
        return:dictionary containing job details
        '''
        jo = self.driver.find_element_by_class_name("jobs-unified-top-card__content--two-pane")
        link = jo.find_element_by_xpath('.//a').get_attribute("href")
        job_prof = jo.find_element_by_xpath('.//a/h2').text
        try:
            company_name = jo.find_element_by_xpath('.//div[1]/span[1]/span[1]/a').text
            company_profile = jo.find_element_by_xpath('.//div[1]/span[1]/span[1]/a').get_attribute("href")
        except:
            company_name = jo.find_element_by_xpath('.//div[1]/span[1]/span[1]').text
            company_profile = "Not Defined"
        location = jo.find_element_by_xpath('.//div[1]/span[1]/span[2]').text
        time_post = jo.find_element_by_xpath('.//div[1]/span[2]/span').text
        date_time = datetime.now()
        job_det = {"Company_Name": company_name,
                   "Company_Profile": company_profile,
                   "Job_profile": job_prof,
                   "Job_Link": link,
                   "Location": location,
                   "Time_of_Post": time_post,
                   "Time_of_scrap":date_time
                   }
        return job_det

    def jobs(self,job_name):
        '''
            It scrape and store all the deatils of jobs from every page
            job_name:string of job which we want to scrape.
         return:list containing dictionary
        '''
        try:
            self.search_filter(job_name)
            j = 0
            jobs_det = []
            pg_2 = []
            while j < 2:
                if j == 0:
                    time.sleep(1)
                    self.scroll()
                    self.scroll()
                    pg_2.append(self.pages())
                    jo = self.job_cont()
                    for i in jo:
                        i.click()
                        jobs_det.append(self.job_detail())
                    j += 1
                else:
                    # It will handle if there is only page for job container
                    if len(pg_2) == 0:
                        break
                    else:
                        pg_2[0].click()
                        time.sleep(1)
                        self.scroll()
                        self.scroll()
                        jo = self.job_cont()
                        for i in jo:
                            i.click()
                            jobs_det.append(self.job_detail())
                        j += 1
                logging.info("Successfully scrape the jobs ")
            return jobs_det
        except Exception as e:
            logging.error("Got an error while scrapping jobs",e)

    def move_back(self, input):
        ''' It will move our driver on Home page '''
        try:
            if (input == "y") or (input == "Y"):
                WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="app-aware-link "]'))
                ).click()
            logging.info("Back on homepage for another job")
        except Exception as e:
            logging.info(e)