import time
import os
import json
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


options = Options()
options.add_argument("--headless")
driver =webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
#driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
wait = WebDriverWait(driver, 10)


def login():
    load_dotenv()
    email = os.getenv('FB_USERNAME')
    password = os.getenv('FB_PASSWORD')
    driver.get('https://facebook.com/')
    driver.find_element('xpath', '//*[@id="email"]').send_keys(email)
    driver.find_element('xpath', '//*[@id="pass"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '[name="login"]').click()
    driver.get(f'https://m.facebook.com/groups/200453430055131')


def loadPage():
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        pages_loaded = 0

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height
            pages_loaded += 1

            print('pages loaded: ', pages_loaded)

    except Exception as e:
        print(e)


def retrivePosts():

    print('parsing posts...')

    posts = driver.find_element(By.ID, 'm_group_stories_container').find_elements(By.TAG_NAME, 'article')
    posts_post_postin = []

    for post in posts:
        user_name = lookupXpath(post, './/div/header/div/div[2]/div/div/div/div[1]/h3/span/strong[1]/a')
        track_title = lookupXpath(post, './/div/div[2]/section/section/div/div/header/h3/span/span')
        text = lookupXpath(post, './/div/div[1]/div/span/p')
        link = lookupXpath(post, './/div/div[2]/section/a')
        date = lookupXpath(post, './/div/header/div/div[2]/div/div/div/div[1]/div/a/abbr')
        reacts = lookupXpath(post, './/footer/div/div[1]/a/div/div[1]/div')
        # comment_count = lookupXpath(post, './/footer/div/div[1]/a/div/div[2]/span')

        post_data = {}

        if user_name:
            post_data['user_name'] = user_name.text
        if track_title:
            post_data['track_title'] = track_title.text
        if text:
            post_data['text'] = text.text
        if link:
            post_data['link'] = link.get_attribute('href')
        if date:
            post_data['date'] = date.text
        if reacts:
            post_data['reacts'] = reacts.text
        # if comment_count:
        #     post_link = lookupXpath(post, '/html/body/div[1]/div/div[4]/div/div/div[4]/section/article[20]/div/div[1]/a')
        #     if post_link:

        posts_post_postin.append(post_data)
    
    return posts_post_postin


def lookupXpath(partent, path):
    try:
        return partent.find_element('xpath', path)
    except:
        return None


def writeJson(posts):
    print('writing posts...')
    with open('gt_posts.json', 'w') as f:
        json.dump(posts, f)


def main():
    login()
    loadPage()
    writeJson(retrivePosts())
    print('done!')

main()


#!/usr/bin/env python3
# from selenium import webdriver
# from selenium.common.exceptions import *
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# chrome_options = Options()
# chrome_options.add_argument("--headless")
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

# driver.get(f"https://www.facebook.com/groups/120778514747417")
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# time.sleep(1)
# posts = driver.find_elements_by_css_selector("div[role='article']")
# for post in posts:
#     labelled_by = post.get_attribute("aria-labelledby")
#     print(labelled_by)
#     label = driver.find_element_by_id(labelled_by).text
#     print(label)
#     desc_by = post.get_attribute("aria-describedby").split()
#     for desc_elem in desc_by:
#         print(desc_elem)
#         try:
#             label = driver.find_element_by_id(desc_elem).text
#             if label:
#                 print(label.strip())
#         except NoSuchElementException:
#             pass