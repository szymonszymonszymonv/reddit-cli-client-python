import requests
import pandas as pd
from requests.api import get
from auth import headers

import json
from comment import Comment
from post import Post


requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


def get_author_details():
    pass

def get_post_details(subreddit, id):
    params = {'article': id}
    query = f'http://oauth.reddit.com/r/{subreddit}/comments/article'
    res = requests.get(query, headers=headers, params=params)
    comments = []
    for c in res.json()[1]['data']['children']:
        c = c['data']
        
        ### TODO: if replies available: find all children and make a tree
        if c['replies']:
            pass
            
        comment = Comment(c['id'], c['body'], c['author'], c['score'])
        comments.append(comment.__dict__)
    return comments
    
def get_posts(subreddit, limit):
    params = {'limit': limit}
    query = f'http://oauth.reddit.com/r/{subreddit}/hot'
    res = requests.get(query, headers=headers, params=params)
    post_list = []
    for p in res.json()['data']['children']:
        p = p['data']
        post = Post(p['title'], p['subreddit'], p['score'], p['author_fullname'], p['selftext'], p['id'])
        comments = get_post_details(post.subreddit, post.id)
        post.set_comments(comments)
        post_list.append(post)
    return post_list

