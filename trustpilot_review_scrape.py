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
driver = get_chromedriver(options=option_arguments)

reviews_list = []
company_dict = {"bsscommerce.com": "BSS Commerce"
                ,"www.magestore.com": "Magestore"}
review_index = [4,7] + list(range(8,31))
for key, value in company_dict.items():
    count = 1
    while True:
        if count == 1:
            trustpilot_link = 'https://www.trustpilot.com/review/{a}?languages=all&sort=recency'.format(a=str(key))   
            driver.get(trustpilot_link) 
            try:
                accept_cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
                accept_cookie_button.click()
                driver.refresh()
            except:
                print("Can't find the 'Got it' button to accept cookie")
                pass  
        else:
            pass
        
        time.sleep(5)
        all_button = driver.find_elements(By.NAME,"review-stack-show")  
        for button in all_button:
            try:
                time.sleep(3)
                button.click()
            except Exception as error_that_has_been_catched:
                print(error_that_has_been_catched)
                continue

        for i in review_index:
            for j in range(1,10):
                try:
                    reviewers = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/aside/div/a/span'.format(str(i))).text
                    country = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/aside/div/a/div/div/span'.format(str(i))).text
                    Rate = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[1]/div[1]/img'.format(str(i))).get_attribute("alt")
                    No_of_reviews = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/aside/div/a/div/span'.format(str(i))).text
                    try:
                        Updated_At = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[1]/div[2]/time'.format(str(i))).get_attribute("title")
                    except:
                        Updated_At = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[1]/div[2]/span/time'.format(str(i))).get_attribute("title")
                    user_link = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/aside/div/a'.format(str(i))).get_attribute("href")

                    try:                                     
                        Date = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[2]/p[2]'.format(str(i))).text
                    except:
                        Date = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[2]/p'.format(str(i))).text
                    review_link = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[2]/a'.format(str(i))).get_attribute("href")
                    title = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[2]/a'.format(str(i))).text

                    try:                                        
                        content = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{}]/article/div/section/div[2]/p[1]'.format(str(i))).text
                    except:
                        content = "No value"
                    Review_item = {
                            "Reviewers": reviewers,
                            'Country': country,
                            'Rate': Rate,
                            'Date of experience': Date,
                            'Updated At': Updated_At,
                            'Number of Reviews in Trustpilot': No_of_reviews,
                            'User link': user_link,
                            'Title': title,
                            'Content': content,
                            'Review link': review_link,
                            "Strapi Team Name": value
                        }
                    reviews_list.append(Review_item)
                except:
                    continue                                
                
                try:                                                  
                    show_more_button = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/button').text
                except:
                    show_more_button = ""
                if len(show_more_button) == 0:
                    break
                
                try:      #for reviews that need clicking to be shown                        
                    title2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[2]/a').text
                    review_link2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[2]/a').get_attribute("href")
                    Rate2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[1]/div[1]/img').get_attribute("alt")
                    reviewers2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/article/div/aside/div/a/span').text
                    user_link2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/article/div/aside/div/a').get_attribute("href")
                    country2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/article/div/aside/div/a/div/div/span').text
                    No_of_reviews2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/article/div/aside/div/a/div/span').text
                    try:
                        Updated_At2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[1]/div[2]/time').get_attribute("title")
                    except:
                        Updated_At2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[1]/div[2]/span/time').get_attribute("title")

                    try:                                     
                        Date2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[2]/p[2]').text
                    except:                                  
                        Date2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[2]/p').text
                    try:                                          
                        content2 = driver.find_element(By.XPATH,f'//*[@id="__next"]/div/div/main/div/div[4]/section/div[{i}]/div/div/article[{j}]/div/section/div[2]/p[1]').text
                    except:
                        content2 = "No value"
                    Review_item = {
                            "Reviewers": reviewers2,
                            'Country': country2,
                            'Rate': Rate2,
                            'Date of experience': Date2,
                            'Updated At': Updated_At2,
                            'Number of Reviews in Trustpilot': No_of_reviews2,
                            'User link': user_link2,
                            'Title': title2,
                            'Content': content2,
                            'Review link': review_link2,
                            "Strapi Team Name": value
                        }
                    reviews_list.append(Review_item)
                except:
                    title2 = ""
                if len(title2) == 0:
                    break
        print(f"{value} - Page {count}: Done")
        count += 1
        try:
            driver.find_element(By.XPATH,"(//a[@name='pagination-button-next'])[1]").click()
        except:
            break
        if date.today().day != 6:
            if count > 3:
                break
        else:
            continue
df = pd.DataFrame(reviews_list)
df= df.drop_duplicates(ignore_index=True)
df['Date of experience'] = df['Date of experience'].replace(regex=['Date of experience: '],value='')
df.loc[df['Content'].str.contains('Date of experience'), 'Content'] = 'No value'
df['Rate'] = df['Rate'].replace(regex=[' out of 5 stars'],value='')
df['Rate'] = df['Rate'].replace(regex=['Rated '],value='')
df['Updated At'] = df['Updated At'].apply(lambda x: x[:x.find(" at")])
df['Updated At'] = df['Updated At'].apply(lambda x: x[(x.find("day, ") + 5):])
df['Number of Reviews in Trustpilot'] = df['Number of Reviews in Trustpilot'].apply(lambda x: x[:x.find(" ")])

review = list(df.to_dict(orient="index").values())
#Append Reviews:
requests.post("https://n8n.magestore.com/webhook/xxxxxxxxxx",
              #headers=auth,
            json = review)


#Update Review status (deleted):
if date.today().day == 2:
    requests.post("https://n8n.magestore.com/webhook/yyyyyyyyyyyyyy",
              #headers=auth,
            json = review)
