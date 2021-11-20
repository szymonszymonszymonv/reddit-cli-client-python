import requests
import pandas as pd
# from rich import print
from rich.console import Console
from rich.json import JSON

CLIENT_ID = 'kdVil3FmFcOUH925cludeA'
SECRET_KEY = 'jcqqk3Kn-SATemNojAx3NLyHwZcYlQ'
# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'project_cli',
        'password': 'reddit123'}

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'cli_project/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)


print(res.json())
# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers['Authorization'] = f'bearer {TOKEN}'

print(headers)
# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)


# print(requests.get('https://oauth.reddit.com/api/v1/me', headers=headers).json())

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