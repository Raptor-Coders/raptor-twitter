import sqlite3

conn = sqlite3.connect('tweets.db', check_same_thread=False)
cursor = conn.cursor()


def init():

  cursor.execute('''CREATE TABLE if not exists tweets (
         _id integer primary key autoincrement, 
         tweet text, 
         username text
       )
    ''')

  cursor.execute('''CREATE TABLE if not exists users (
          _id integer primary key autoincrement, 
          username text, 
          password text, 
          UNIQUE(username)
       )
    ''')

  cursor.execute('''CREATE TABLE if not exists followers (
         follower INTEGER NOT NULL,
         followee INTEGER NOT NULL,
         FOREIGN KEY (follower) REFERENCES user(id),
         FOREIGN KEY (followee) REFERENCES user(id),
         PRIMARY KEY (follower, followee)
      )
    ''')

  cursor.execute('''CREATE TABLE if not exists likes (
         user_id integer, 
         tweet_id integer, 
         created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
         FOREIGN KEY (user_id) REFERENCES users(_id),
         FOREIGN KEY (tweet_id) REFERENCES tweets(_id),
         PRIMARY KEY (user_id, tweet_id)
      )
    ''')

  conn.commit()


def is_liked_by_user(user_id, tweet_id):
  cursor.execute(
    'SELECT * FROM likes where user_id = :user_id AND tweet_id = :tweet_id', {
      'user_id': user_id,
      'tweet_id': tweet_id
    })

  # return cursor.fetchone() is not None
  
  if cursor.fetchone():
    return True
  else:
    return False


def like_tweet(user_id, tweet_id):
  cursor.execute(
    'INSERT INTO likes (user_id, tweet_id) VALUES (:user_id, :tweet_id)', {
      'user_id': user_id,
      'tweet_id': tweet_id
    })

  conn.commit()


def get_likes_count(tweet_id):
  cursor.execute('SELECT COUNT(user_id) FROM likes where tweet_id = :tweet',
                 {'tweet': tweet_id})
  likes = cursor.fetchone()
  return likes


def get_all_likes(limit):
  cursor.execute('SELECT * FROM likes')
  return cursor.fetchmany(limit)


def follow_user(follower, followee):
  cursor.execute('INSERT INTO followers VALUES (:follower, :followee)', {
    'follower': follower,
    'followee': followee,
  })

  conn.commit()


def unfollow_user(follower, followee):
  cursor.execute(
    'DELETE FROM followers WHERE follower = :follower and followee = :followee',
    {
      'follower': follower,
      'followee': followee
    })

  conn.commit()


def unlike_tweet(user_id, tweet_id):
  cursor.execute(
    'DELETE FROM likes WHERE user_id = :user_id and tweet_id = :tweet_id', {
      'user_id': user_id,
      'tweet_id': tweet_id
    })

  conn.commit()


def get_all_users_following(userid):
  cursor.execute(
    'SELECT * FROM users where _id in (SELECT followee from followers where follower = :a)',
    {'a': userid})

  followers = cursor.fetchall()

  return followers


def get_all_users_unfollowing(userid):
  sql = '''
    SELECT * 
    FROM users 
    where 
      _id NOT IN (SELECT followee from followers where follower = :a)
      AND _id <> :a
  '''
  cursor.execute(sql, {'a': userid})

  followers = cursor.fetchall()

  return followers


def get_all_users_unfollowing_BACKUP(userid):
  """
  Returns a list of users that the user in question is not following
  :param userid:
  :return: []
  """
  # Get the list of users following the given user
  cursor.execute('SELECT follower FROM followers WHERE followee = :userid',
                 {'userid': userid})

  # Above query returned a list of tuples [(2,), (3,)] so access the index 0 to get the id
  followers = [row[0] for row in cursor.fetchall()]

  # Get the list of all users and exclude himself since he can not follow himself
  all_users = get_all_users()
  all_other_users = [row for row in all_users if row[0] != userid]

  # Find the users not in the followers list
  users_not_following = [
    user for user in all_other_users if user[0] not in followers
  ]

  return users_not_following


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


def get_famous_tweets(limit):
  cursor.execute('''SELECT tweet_id, COUNT(user_id) AS cnt
                    FROM likes 
                    GROUP BY tweet_id
                    ORDER BY cnt DESC''')
  # add join to fetch username and tweet text
  # refactor famous_tweets.html to account to additional field being returned
  #cursor.execute('''SELECT twt.username, twt.tweet, COUNT(likes.user_id) AS cnt  
  #                  FROM likes 
  #                  INNER JOIN tweets twt
  #                  ON twt._id = likes.tweet_id
  #                  GROUP BY likes.tweet_id
  #                  ORDER BY cnt DESC''')
  famouslikes = cursor.fetchmany(limit)
  return famouslikes