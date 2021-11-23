import json


class Post():
    def __init__(self, title: str, subreddit: str, score: int, author: str, selftext: str, id: str, time_ago: int):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.author = author
        self.selftext = selftext
        self.id = id
        self.comments = []
        self.time_ago = time_ago
        
    def build_from_json():
        posts = []
        with open('response.json', 'r') as file:
            data = json.load(file)
            for post in data:
                p = Post(post['title'], post['subreddit'], post['score'], post['author'], post['selftext'], post['id'])
                posts.append(p)
        return posts
        
    def set_comments(self, comments):
        self.comments = comments
        
    def __str__(self):
        return f"[b]{self.author} - /r/{self.subreddit} ({self.time_ago})\n[orange3]{self.title}\n[orange1]score: {self.score}"