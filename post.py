
class Post():
    def __init__(self, title: str, subreddit: str, score: int, author_fullname: str, selftext: str, id: str):
        self.title = title
        self.subreddit = subreddit
        self.score = score
        self.author_fullname = author_fullname
        self.selftext = selftext
        self.id = id
        self.comments = []
        
        
    def set_comments(self, comments):
        self.comments = comments
        
    def __str__(self):
        return f"{self.title}\n{self.score}"