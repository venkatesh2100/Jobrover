from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pymongo import MongoClient
import time

options = webdriver.ChromeOptions()
service = Service("/usr/bin/chromedriver")
# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["linkedin_bot"]
applications = db["applications"]

# Selenium WebDriver Setup
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=options)

def login(email, password):
    driver.get("https://www.linkedin.com/login")
    time.sleep(2)

    driver.find_element(By.ID, "username").send_keys(email)
    driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)
    time.sleep(5)

def search_jobs(keyword, location):
    driver.get("https://www.linkedin.com/jobs")
    time.sleep(2)

    search_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search jobs']")
    search_box.send_keys(keyword + Keys.RETURN)
    time.sleep(2)

    location_box = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Search location']")
    location_box.clear()
    location_box.send_keys(location + Keys.RETURN)
    time.sleep(3)

def apply_to_jobs():
    jobs = driver.find_elements(By.CSS_SELECTOR, ".job-card-container")

    for job in jobs:
        try:
            job.click()
            time.sleep(2)

            easy_apply = driver.find_element(By.XPATH, "//button[contains(text(),'Easy Apply')]")
            easy_apply.click()
            time.sleep(2)

            submit_button = driver.find_element(By.XPATH, "//button[contains(text(),'Submit application')]")
            submit_button.click()

            job_title = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__title").text
            company = driver.find_element(By.CSS_SELECTOR, ".top-card-layout__first-subline").text

            applications.insert_one({
                "title": job_title,
                "company": company,
                "applied_at": time.strftime("%Y-%m-%d %H:%M:%S")
            })

            print(f"Applied to: {job_title} at {company}")
            time.sleep(3)
        except Exception as e:
            print(f"Skipping job due to error: {e}")

if __name__ == "__main__":
    email = "email"
    password = "password"

    login(email, password)
    search_jobs("Software Engineer", "Remote")
    apply_to_jobs()

    driver.quit()
