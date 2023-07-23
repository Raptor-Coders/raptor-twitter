import db


def get_all_likes(limit):
  return db.get_all_likes(limit)


def like_tweet(user_id, tweet_id):
  return db.like_tweet(user_id, tweet_id)


def unlike_tweet(user_id, tweet_id):
  return db.unlike_tweet(user_id, tweet_id)


def is_liked_by_user(user_id, tweet_id):
  return db.is_liked_by_user(user_id, tweet_id)


def label_likes_for_user(tweets, user_id):
  labeled_tweets = []
  for tweet in tweets:
    tweet_id = tweet[0]
    is_liked = is_liked_by_user(user_id, tweet_id)
    labeled_tweets.append((tweet[0], tweet[1], tweet[2], is_liked))

  return labeled_tweets
