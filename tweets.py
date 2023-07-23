import db


def get_all_tweets(limit=100):
  return db.get_all_tweets(limit)

def get_famous_tweets(limit):
  return db.get_famous_tweets(limit)

def add_tweet(tweet, username):
  db.create_tweet(username, tweet)


def get_tweets_by_username(username):
  return db.get_tweets_by_username(username)


def is_liked_by_user(user_id, tweet_id):
  return db.is_liked_by_user(user_id, tweet_id)
