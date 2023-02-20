import os
import json
from typing import List, Union
from dotenv import load_dotenv
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
# driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
wait = WebDriverWait(driver, 120)


def login() -> None:
    load_dotenv()
    email = os.getenv('FB_USERNAME')
    password = os.getenv('FB_PASSWORD')
    driver.get('https://facebook.com/')
    driver.find_element('xpath', '//*[@id="email"]').send_keys(email)
    driver.find_element('xpath', '//*[@id="pass"]').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '[name="login"]').click()
    driver.get(f'https://m.facebook.com/groups/200453430055131')
    


def lookupXpath(parent: WebElement, path: str) -> Union[WebElement, None]:
    try:
        return parent.find_element('xpath', path)
    except:
        return None


def assertNextPageLoading(group_stories_container: WebElement) -> bool:
    next_section = lookupXpath(group_stories_container, './div')
    try:
        if not next_section:
            return False
        return next_section.get_attribute('id') == "m_more_item"
    except:
        return False


def loadPagesAndParse() -> None:
    try:
        group_stories_container = driver.find_element('xpath', '//*[@id="m_group_stories_container"]')
        last_height = driver.execute_script("return document.body.scrollHeight")
        pages_loaded = 0

        while True:

            section_data = retrivePosts(group_stories_container)
            print(section_data)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait.until(lambda _: not assertNextPageLoading(group_stories_container))
            new_height = driver.execute_script("return document.body.scrollHeight")
    
            if new_height == last_height:
                break

            last_height = new_height
            group_stories_container = lookupXpath(group_stories_container, './/*[@id="m_group_stories_container"]')
            pages_loaded += 1

            print('pages loaded: ', pages_loaded)

    except Exception as e:
        print(e)


def retrivePosts(group_stories_container: WebElement) -> Union[List[any], None]:
    if not group_stories_container:
        return

    posts = group_stories_container.find_elements(By.TAG_NAME, 'article')
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
            post_data['link'] = parseLink(link.get_attribute('href'))
        if date:
            post_data['date'] = date.text
        if reacts:
            post_data['reacts'] = parseReacts(reacts.text)
        else:
            post_data['reacts'] = 0
        # if comment_count:
        #     post_link = lookupXpath(post, '/html/body/div[1]/div/div[4]/div/div/div[4]/section/article[20]/div/div[1]/a')
        #     if post_link:

        posts_post_postin.append(post_data)

    return posts_post_postin


def parseReacts(reacts: str) -> int:
    def parse(reacts: List[str], i: int, inName: bool) -> int:
        if i >= len(reacts):
            return 0
        if reacts[i].isdigit():
            return int(reacts[i]) + parse(reacts, i + 1, False)
        if reacts[i] == 'and' or reacts[i] == 'others':
            return parse(reacts, i + 1, False)
        if inName:
            return parse(reacts, i + 1, True)
        else:
            return 1 + parse(reacts, i + 1, True)

    return parse(reacts.split(' '), 0, False)


def parseLink(url: str) -> str:
    start_trimmed = url[32:]
    return unquote(start_trimmed[:start_trimmed.find('&h=')])


def writeJson(posts: List[any]) -> None:
    print('writing posts...')
    with open('gt_posts.json', 'w') as f:
        json.dump(posts, f)


login()
loadPagesAndParse()
print('done!')