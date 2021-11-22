import json


class Comment():
    def __init__(self, id: int, comment: str, author: str, score: int, parent = -1):
        self.id = id
        self.comment = comment
        self.author = author
        self.score = score
        self.parent = parent
        
    def build_from_json(filename):
        comments = []
        with open(filename, 'r') as file:
            data = json.load(file)
            for c in data:
                comment = Comment(c['id'], c['comment'], c['author'], c['score'])
                comments.append(comment)
        return comments
    
    def build_from_dict(dict):
        comment = Comment(
            dict['id'],
            dict['comment'],
            dict['author'],
            dict['score']
            )
        return comment
        

    def __str__(self):
        return f"[orange4]{self.author} | [orange1]score: {self.score}\n[orange3]{self.comment} "
    