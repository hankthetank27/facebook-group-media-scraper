import json
import os
from facebook_scraper import get_posts
from dotenv import load_dotenv

load_dotenv()
email = os.getenv('FB_USERNAME')
password = os.getenv('FB_PASSWORD')

def writeJson(posts):
    with open('gt_posts.json', 'w') as f:
        json.dump(posts, f)

posts = []
try:
    for post in get_posts('200453430055131', pages=99999, credentials=(email, password), options={'comments': True, 'posts_per_page' : 200, 'allow_extra_requests': False}, extra_info=True):
        print(post['post_id'], post['comments_full'])
        post_data = {
            'post_id' : post['post_id'],
            'username' : post['username'],
            'post_text' : post['post_text'],
            'link' : post['link'],
            'reactions' : post['reactions'],
            'comments' : post['comments'],
            'comments_full': [
                {
                    'commenter_name': c['commenter_name'],
                    'comment_text' : c['comment_text'],
                    'replies' : [r for r in c['replies']]
                } for c in post['comments_full']]
        }
        posts.append(post_data)
    writeJson(posts)
except:
    writeJson(posts)


