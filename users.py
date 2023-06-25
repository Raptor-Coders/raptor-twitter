import db
from werkzeug.security import generate_password_hash, check_password_hash


def password_match(username, password) -> bool:
  (id, user, pw) = get_user_by_username(username)
  return check_password_hash(pw, password)


def follow_user(follower, followee):
  '''
    Perform checks
  '''
  # if all good, call db function
  db.follow_user(follower, followee)


def unfollow_user(follower, followee):
  '''
    Perform checks
  '''
  # if all good, call db function
  db.unfollow_user(follower, followee)


def get_all_users():
  return db.get_all_users()


def get_all_users_following(user_id):
  return db.get_all_users_following(user_id)


def get_all_users_unfollowing(user_id):
  return db.get_all_users_unfollowing(user_id)


def create_user(username, password):
  hashed_password = generate_password_hash(password, method="sha256")
  db.create_user(username, hashed_password)


def get_user_by_username(username):
  return db.get_user_by_username(username)
