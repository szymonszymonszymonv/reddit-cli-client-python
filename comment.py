class Comment():
    def __init__(self, id: int, comment: str, author: str, score: int, parent = -1):
        self.id = id
        self.comment = comment
        self.author = author
        self.score = score
        self.parent = parent
        
    def __str__(self):
        return f"{self.author} | {self.score}\n{self.comment} "