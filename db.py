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

  cursor.execute(
    '''
      CREATE TABLE if not exists followers (
        follower INTEGER NOT NULL,
        followee INTEGER NOT NULL,
        FOREIGN KEY (follower) REFERENCES user(id),
        FOREIGN KEY (followee) REFERENCES user(id),
        PRIMARY KEY (follower, followee)
      );
    '''
  )
  conn.commit()


def follow_user(follower, followee):
  cursor.execute('INSERT INTO followers VALUES (:follower, :followee)', {
    'follower': follower,
    'followee': followee,
  })

  conn.commit()


def get_all_users_following(userid):
  cursor.execute('SELECT * from followers where followee = :a', {
    'a': userid
  })

  followers = cursor.fetchall()

  return followers


def get_all_users_unfollowing(userid):
  """
  Returns a list of users that the user in question is not following
  :param userid:
  :return: []
  """
  # Get the list of users following the given user
  cursor.execute('SELECT follower FROM followers WHERE followee = :userid', {'userid': userid})

  # Above query returned a list of typle [(2,), (3,)] so access the index 0 to get the id
  followers = [row for row in cursor.fetchall()]

  # Get the list of all users and exclude himself since he can not follow himself
  all_users = get_all_users()
  all_other_users = [row for row in all_users if row[0] != userid]

  follower_ids = [follower[0] for follower in followers]

  # Find the users not in the followers list
  users_not_following = [user for user in all_other_users if user[0] not in follower_ids]


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
