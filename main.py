import requests
import pandas as pd
from auth import headers
# from rich import print
from rich.console import Console
from rich.json import JSON


print(headers)
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)



res = requests.get('http://oauth.reddit.com/r/python/hot', headers=headers, params={'limit': '50'}) # limit w ilosci postow wyswietlanych
print("xD")


df = pd.DataFrame()

for post in res.json()['data']['children']:
    df = df.append({
        'subreddit': post['data']['subreddit'],
        'title': post['data']['title'],
        'selftext': post['data']['selftext'],
        'upvote_ratio': post['data']['upvote_ratio'],
        'ups': post['data']['ups'],
        'downs': post['data']['downs'],
        'score': post['data']['ups']
    }, ignore_index=True)