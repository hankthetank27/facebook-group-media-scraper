import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
wait = WebDriverWait(driver, 10)

def login():
    load_dotenv()
    email = os.getenv('FB_USERNAME')
    password = os.getenv('FB_PASSWORD')
    driver.get('https://facebook.com/')
    driver.find_element('xpath', '//*[@id="email"]').send_keys(email)
    driver.find_element('xpath', '//*[@id="pass"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '[name="login"]').click()

def goToGroup():
    driver.get('https://www.facebook.com/groups/200453430055131')

def retrivePosts():
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    count = 0
    while True and count < 1:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(2)
        #or...
        #wait.until(EC. ....)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height

        #remove
        count += 1

    return driver.find_elements(By.CSS_SELECTOR, '[role="article"]')

def parseFeed(posts):
       
    for post in posts:
        links = post.find_elements(By.TAG_NAME, 'a')
        for link in links:
            
            print(link.get_attribute('href'))


#feed
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[2]/div'


#fist item
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[2]/div/div[2]'

#article
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div/div/div'

#link
'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div[2]/div/div/div[4]/div/div[2]/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div/div/div/div/div/div[8]/div/div/div[3]/div[2]/div[1]/div[1]/div/a'



# login()
# goToGroup()
# posts = retrivePosts()
# parseFeed(posts)