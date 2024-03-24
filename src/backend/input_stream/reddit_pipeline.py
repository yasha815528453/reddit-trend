import praw
import threading
import os
from database import models

class RedditStreamer:
    def __init__(self, interested_subreddits, lang_processer):
        self.reddit_client = praw.Reddit(
            client_id = os.getenv("CLIENT_ID"),
            client_secret = os.getenv("CLIENT_SECRET"),
            user_agent = os.getenv("USER_AGENT"),
        )
        self.subreddits = interested_subreddits
        self.lang_processer = lang_processer



    ## refer to https://praw.readthedocs.io/en/stable/code_overview/models/submission.html
    ## for comment and submission attributes

    def stream_submissions(self, queue) -> None:
        for submission in self.reddit_client.subreddit(self.subreddits).stream.submissions():
            keywords = self.lang_processer.extract_keywords(submission.title)
            print(f"New post in {submission.subreddit}: {submission.title}")
            for keyword in keywords:
                queue.put(models.RedditPost(keyword, submission.id, 1, True, submission.subreddit.display_name).to_tuple())



    def stream_comments(self, queue) -> None:
        for comment in self.reddit_client.subreddit(self.subreddits).stream.comments():
            keywords = self.lang_processer.extract_keywords(comment.body)
            print(f"New comment in {comment.subreddit}: {comment.body}")
            for keyword in keywords:
                queue.put(models.RedditComment(keyword, comment.id, 1, False, comment.subreddit.display_name).to_tuple())
