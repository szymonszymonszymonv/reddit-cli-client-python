import datetime
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
    params = {'article': id, 'limit':10}
    query = f'http://oauth.reddit.com/r/{subreddit}/comments/article'
    res = requests.get(query, headers=headers, params=params)
    comments = []
    for c in res.json()[1]['data']['children']:
        c = c['data']
        
        ### TODO: if replies available: find all children and make a tree
        # if c['replies']:
        #     pass.
        try:
            comment = Comment(c['id'], c['body'], c['author'], c['score'])
            comments.append(comment.__dict__)
        except:
            continue
        
    return comments
    
def get_posts(subreddit, limit, after="", before=""):
    params = {'limit': limit, "after":after, "before":before}
    query = f'http://oauth.reddit.com/r/{subreddit}'
    res = requests.get(query, headers=headers, params=params)
    post_list = []
    for p in res.json()['data']['children']:
        p = p['data']
        # calculate when the post was created
        dif_time = datetime.datetime.now() - datetime.datetime.fromtimestamp(p['created_utc'])
        hours = round(dif_time.total_seconds() / 3600)
        time_ago = ""
        if hours < 24:
            time_ago = f"{hours} hours ago"
        else:
            days = round(hours / 24)
            time_ago = f"{days} days ago" 
            
        selftext = p['selftext']
        try:
            selftext = p['url_overridden_by_dest']
        except:
            pass
        
        post = Post(p['title'], p['subreddit'], p['score'], p['author'], selftext, p['id'], time_ago)
        comments = get_post_details(post.subreddit, post.id)
        post.set_comments(comments)
        post_list.append(post)
    return post_list


def write_to_file(collection, filename):
    with open(filename, 'w') as file:
        file.write('[')
        for i in range(0, len(collection)):
            item = collection[i]
            with open(f"{i}comments_{filename}", 'w') as file2:
                file2.write('[')
                for i in range(0, len(item.comments)):
                    json.dump(item.comments[i], file2)
                    if i != len(item.comments) - 1:
                        file2.write(',')
                file2.write(']')
                            
            json.dump(item.__dict__, file)
            if i != len(collection) - 1:
                file.write(',')
        file.write(']')
