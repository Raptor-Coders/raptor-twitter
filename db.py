import sqlite3

conn = sqlite3.connect('tweets.db', check_same_thread=False)
cursor = conn.cursor()


def init():
  cursor.execute(
    '''CREATE TABLE if not exists tweets (_id integer primary key autoincrement, tweet text, username text)'''
  )
  cursor.execute(
    '''CREATE TABLE if not exists users (_id integer primary key autoincrement, username text, password text, UNIQUE(username))'''
  )
  conn.commit()


def create_tweet(username, tweet):
  cursor.execute('INSERT INTO tweets VALUES (null, :t, :u)', {
    't': tweet,
    'u': username
  })

  conn.commit()


def create_user(username, password):
  cursor.execute('INSERT INTO users VALUES (null, :u, :p)', {
    'u': username,
    'p': password
  })

  conn.commit()


def get_all_tweets(limit):
  cursor.execute('SELECT * FROM tweets order by _id desc')
  tweets = cursor.fetchmany(limit)
  return tweets


def get_tweets_by_username(username):
  cursor.execute('SELECT * FROM tweets WHERE username = :username',
                 {'username': username})
  tweets = cursor.fetchmany(10)

  return tweets


def get_user_by_username(username):
  cursor.execute('SELECT * FROM users WHERE username = :username',
                 {'username': username})
  user = cursor.fetchone()

  return user


def get_all_users():
  cursor.execute('SELECT * FROM users order by _id desc')
  users = cursor.fetchall()
  return users


def get_all_users_following():
  return []


def get_all_users_unfollowing():
  return []