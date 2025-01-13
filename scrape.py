import time
import datetime
from datetime import date
from datetime import datetime, timedelta

#Open Chrome
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import Dict, List

#clean data
import pandas as pd
import gspread
import pygsheets
import numpy as np
from dateutil.relativedelta import relativedelta

#Request Webhook
import requests

#Other Function
from utilities.path import absolute_path
from utilities.scrape_utils import get_chromedriver, webdriver_manager_env
#To hide the credential
from config import option_arguments
import json
def get_auth(path):
    with open(path, "r") as f:
        return json.load(f)

webdriver_manager_env()
try:
    driver = get_chromedriver(options=option_arguments)
except:
    driver = webdriver.Chrome(executable_path="C:/Users/BSS/chromedriver.exe")
driver.maximize_window()

def resolve_showmore_button(review_section: WebElement, driver: WebDriver) -> None:
    button = review_section.find_element(By.TAG_NAME, "button")
    if button.text.strip() == "Show more":
        # if the comment section has a "Show more" button 
        # the driver will scroll to that comment section and click on that button.
        driver.execute_script("arguments[0].scrollIntoView();", review_section)
        time.sleep(2)
        driver.execute_script("window.scrollBy(0,10)")
        button.click()
        time.sleep(2)

def review_content(review_section: WebElement, driver: WebDriver ) -> str:
    resolve_showmore_button(review_section, driver)
    return review_section.text.strip()
        


app_dict = { 
    'Product Label': 'https://apps.shopify.com/product-labels-by-bss/reviews?sort_by=newest&page='
    ,'Login to Access': 'https://apps.shopify.com/login-to-access-pages/reviews?sort_by=newest&page='
    ,'B2B Solution': 'https://apps.shopify.com/b2b-solution-custom-pricing/reviews?sort_by=newest&page='
    ,'Product Option': 'https://apps.shopify.com/product-options-by-bss/reviews?sort_by=newest&page='
    ,'Bloop': 'https://apps.shopify.com/bloop-loyalty/reviews?sort_by=newest&page='
    ,'Customer Portal': 'https://apps.shopify.com/b2b-customer-portal-quick-order/reviews?sort_by=newest&page='
    ,'Store Locator': 'https://apps.shopify.com/dealer-store-locator/reviews?sort_by=newest&page='
    ,'Mida': 'https://apps.shopify.com/mida-session-recording-replay/reviews?sort_by=newest&page='
    ,'Subscription': 'https://apps.shopify.com/subscription-recurring-pay/reviews?sort_by=newest&page='
}
review_list = []
element_index = [2,4,6,7,8,9,10,11,12,13]
for app_name, app_link in app_dict.items():
    count = 1
    while True:
        driver.get(f'{app_link}{str(count)}')
        time.sleep(3)                                      
        try:                                              
            check_review = driver.find_element(By.XPATH, '/html/body/main/section/div/div[3]/div[2]/div[2]/div[2]/div[1]').get_attribute("data-review-content-id")
            button_list = driver.find_elements(By.XPATH, "/html/body/main/section/div/div[3]/div[2]/div[2]/div[*]/div[1]/div[1]/div[2]")
        except:
            try:
                check_review = driver.find_element(By.XPATH, '/html/body/main/section/div/div[3]/div[2]/div[3]/div[2]/div[1]').get_attribute("data-review-content-id")
                button_list = driver.find_elements(By.XPATH, "/html/body/main/section/div/div[3]/div[2]/div[3]/div[*]/div[1]/div[1]/div[2]")
            except:
                check_review = "" 
                print(app_name + " Page " +str(count) + ": Can't find element or Page has no reviews")
        if len(check_review) == 0:
            break

        for button in button_list:                   
            try:
                review_content(button, driver)
            except:
                continue

        
        for h in element_index:    
            try: 
                try:
                    merchant = driver.find_element(By.XPATH,"/html/body/main/section/div/div[3]/div[2]/div[1]/div/div[1]/h5").text
                except:
                    merchant = ""
                if merchant == "What merchants think":                       
                        content_id = driver.find_element(By.XPATH, f'/html/body/main/section/div/div[3]/div[2]/div[3]/div[{h}]/div[1]').get_attribute("data-review-content-id")
                        reviewer = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[3]/div[{h}]/div[1]/div[2]/div[1]').text
                        content = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[3]/div[{h}]/div[1]/div[1]/div[2]/div').text
                        review_date = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[3]/div[{h}]/div[1]/div[1]/div[1]/div[2]').text
                        rating = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[3]/div[{h}]/div[1]/div[1]/div[1]/div[1]').get_attribute("aria-label")
                        try:                                             
                            time_spent = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[3]/div[{h}]/div[1]/div[2]/div[3]').text
                        except:                                         
                            time_spent = "0 days using the app"
                        location = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[3]/div[{h}]/div[1]/div[2]/div[2]').text
                else:
                    content_id = driver.find_element(By.XPATH, f'/html/body/main/section/div/div[3]/div[2]/div[2]/div[{h}]/div[1]').get_attribute("data-review-content-id")
                    reviewer = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[2]/div[{h}]/div[1]/div[2]/div[1]').text
                    content = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[2]/div[{h}]/div[1]/div[1]/div[2]/div').text
                    review_date = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[2]/div[{h}]/div[1]/div[1]/div[1]/div[2]').text
                    rating = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[2]/div[{h}]/div[1]/div[1]/div[1]/div[1]').get_attribute("aria-label")
                    try:                                             
                        time_spent = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[2]/div[{h}]/div[1]/div[2]/div[3]').text
                    except:                                         
                        time_spent = "0 days using the app"
                    location = driver.find_element(By.XPATH,f'/html/body/main/section/div/div[3]/div[2]/div[2]/div[{h}]/div[1]/div[2]/div[2]').text
            except:                                                                               
                print(app_name + " Page " +str(count) + ": Can't find element number " + str(h))
                continue
                
            app = app_name
            review_item = {
                        'review_id': content_id,
                        'app_name': app,
                        'reviewer': reviewer,
                        'content': content,
                        'date': review_date,
                        'rating':rating,
                        'time_spent':time_spent,
                        'location':location
            }
            review_list.append(review_item)   

        print(app_name + " Page " +str(count) + ": Done")
        count += 1 

        if date.today().day != 2:
            if count > 3:
                break
        else:
            continue       

df = pd.DataFrame(review_list)

def days_spent(time):
    days_spent =  [int(s) for s in time.split() if s.isdigit()][0]
    dict_time = {"minute": 1/(60*24*30), "hour": 1/(24*30), "day": 1/30, "month": 1, "year": 12}
    for unit in dict_time:
        if unit in time:
            days_spent_clean = days_spent*dict_time[unit]
    if "Over" in time: days_spent_clean=days_spent*1.01
    if"About" in time: days_spent_clean=days_spent*0.99
            
    return days_spent_clean
#Date column
for i in df.index:
    if df.loc[i,'date'].find('Edited') != - 1:
        df.loc[i,'date'] = df.loc[i,'date'].replace('Edited','').strip()
#rating column
for i in df.index:
    df.loc[i,'rating'] = df.loc[i,'rating'].split()[0]
#Convert date_clean to format mm/dd/yyyy
from datetime import datetime
def mdy_to_ymd(d):
    return datetime.strptime(d,'%B %d, %Y').strftime('%Y-%m-%d')
for i in df.index:
    df.loc[i,'date'] = mdy_to_ymd(df.loc[i,'date'])


df = df.sort_values(by = ['app_name','date'])
for i in df.index:
    if df.loc[i,'time_spent'].find(' using the app') != - 1:
        df.loc[i,'time_spent'] = df.loc[i,'time_spent'].replace(' using the app','').strip()
df=df.reset_index()
df["time_spent"] = df["time_spent"].astype(str).apply(days_spent)
df["time_spent"] = df["time_spent"].round(2)
df = df.drop('index', axis=1)
print(df.head(30))
review = list(df.to_dict(orient="index").values())
print(review[:5])
#Append Reviews:
requests.post("https://n8n.magestore.com/webhook/xxxxxxxxxxx",
              #headers=auth,
            json = review)
#Update Review status (deleted):
if date.today().day == 2:
  requests.post("https://n8n.magestore.com/webhook/yyyyyyyyyyy",
              #headers=auth,
            json = review)
