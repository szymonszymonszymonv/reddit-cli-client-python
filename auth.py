from secret import data, CLIENT_ID, SECRET_KEY
import requests

# setup our header info, which gives reddit a brief description of our app
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, SECRET_KEY)
headers = {'User-Agent': 'cli_project/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)


print(res.json())
# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers['Authorization'] = f'bearer {TOKEN}'
