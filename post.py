
class Post():
    def __init__(self, title: str, subreddit: str, score: int, author_fullname: str, selftext: str, id: str):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.author_fullname = author_fullname
        self.selftext = selftext
        self.id = id
        self.comments = []
        
        
        # 'subreddit': post['data']['subreddit'],
        # 'author_fullname': post['data']['author_fullname'],
        # 'name': post['data']['name'],
        # 'title': post['data']['title'],
        # 'selftext': post['data']['selftext'],
        # 'upvote_ratio': post['data']['upvote_ratio'],
        # 'ups': post['data']['ups'],
        # 'downs': post['data']['downs'],
        # 'score': post['data']['ups']
        
    def set_comments(self, comments):
        self.comments = comments