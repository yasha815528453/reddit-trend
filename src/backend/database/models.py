from datetime import datetime


class RedditPost:
    def __init__(self, keyword, id, count, post, subreddit):
        self.subreddit = subreddit
        self.keyword = keyword
        self.id = id
        self.count = count
        self.date = datetime.now().date()
        self.post = post


    def to_tuple(self):
        return (self.keyword, self.date, self.count, self.id, self.post, self.subreddit)


class RedditComment:
    def __init__(self, keyword, post_id, count, post, subreddit):
        self.subreddit = subreddit
        self.keyword = keyword
        self.post_id = post_id
        self.count = count
        self.date = datetime.now().date()
        self.post = post

    def to_tuple(self):
        return (self.keyword, self.date, self.count, self.post_id, self.post, self.subreddit)
