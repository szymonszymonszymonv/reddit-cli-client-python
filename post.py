import json


class Post():
    def __init__(self, title: str, subreddit: str, score: int, author_fullname: str, selftext: str, id: str):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.author_fullname = author_fullname
        self.selftext = selftext
        self.id = id
        self.comments = []
        
    def build_from_json():
        posts = []
        with open('response.json', 'r') as file:
            data = json.load(file)
            for post in data:
                p = Post(post['title'], post['subreddit'], post['score'], post['author_fullname'], post['selftext'], post['id'])
                posts.append(p)
        return posts
        
    def set_comments(self, comments):
        self.comments = comments
        
    def __str__(self):
        return f"[orange3]{self.title}\n[orange1]score: {self.score}"