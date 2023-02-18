import os
from facebook_scraper import get_posts
from dotenv import load_dotenv

load_dotenv()
email = os.getenv('FB_USERNAME')
password = os.getenv('FB_PASSWORD')

for post in get_posts('200453430055131', pages='5', credentials=(email, password)):
    print(post)