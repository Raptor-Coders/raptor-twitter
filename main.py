from flask import Flask, request, redirect, url_for, render_template, session, flash
from tweets import add_tweet, get_all_tweets, get_tweets_by_username
from users import create_user, password_match, get_user_by_username, get_all_users_following, get_all_users_unfollowing, get_all_users, follow_user
import random

app = Flask(__name__)
app.secret_key = 'raptor-secret-key'

from db import init

init()


@app.context_processor
def inject_user():
  username = session.get('user', None)
  return {'username': username}


def get_html_form(action, header, fieldtitle, fieldname, buttonvalue):
  return render_template('form.html',
                         action=action,
                         header=header,
                         fieldtitle=fieldtitle,
                         fieldname=fieldname,
                         buttonvalue=buttonvalue)


@app.route('/')
def index():
  if 'user' in session:
    # Get last 10 tweets
    tweets = get_all_tweets(10)
    return render_template('home.html', tweets=tweets)
  else:
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
  username = request.form['username']
  password = request.form['password']

  if not username or not password:
    flash('Username or password can not be blank!', 'error')
    return render_template('login.html')

  authenticated = password_match(username, password)
  if authenticated:
    session['user'] = username
    flash('Login was successful!', 'info')
    return redirect(url_for('index'))
  else:
    flash('Login Failed. Invalid username or password!', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
  del session['user']
  flash('Logout was successful!', 'info')
  return redirect(url_for('index'))


@app.route('/tweet')
def tweet():
  return render_template('form.html',
                         action='/save-tweet',
                         header='What is happening?',
                         fieldtitle='Tweet',
                         fieldname='tweet',
                         buttonvalue='Tweet')


@app.route('/save-tweet', methods=['POST'])
def contact():
  tweet = request.form['tweet']
  if not tweet:
    flash('Tweet can not be empty!', 'error')
    return render_template('form.html',
                           action='/save-tweet',
                           header='What is happening?',
                           fieldtitle='Tweet',
                           fieldname='tweet',
                           buttonvalue='Tweet')

  if len(tweet) > 250:
    flash('Tweet can not be more than 250 characters long!', 'error')
    return render_template('form.html',
                           action='/save-tweet',
                           header='What is happening?',
                           fieldtitle='Tweet',
                           fieldname='tweet',
                           buttonvalue='Tweet')

  add_tweet(tweet, session['user'])
  flash('Successfully posted successfully!', 'info')
  return redirect(url_for('index'))


@app.route('/tweets/<tweet_user>')
@app.route('/tweets')
def user_tweets(tweet_user=None):
  if 'user' not in session:
    return redirect(url_for('index'))

  if tweet_user:
    tweets = get_tweets_by_username(tweet_user)
  else:
    tweets = get_all_tweets()

  return render_template('tweets_page.html',
                         tweets=tweets,
                         tweet_user=tweet_user)


@app.route('/register', methods=['GET'])
def register():
  return render_template('register.html')


@app.route('/register-post', methods=['POST'])
def register_post():
  username = request.form['username']
  password = request.form['password']

  if not username or not password:
    flash('Username or password can not be blank!', 'error')
    return render_template('register.html')

  try:
    create_user(username, password)
    get_user_by_username(username)
  except Exception as e:
    flash(f'Error registering {username}: {e}', 'error')
    return render_template('register.html')
  else:
    flash(f'Successfully registered {username}', 'info')
    return redirect(url_for('index'))


@app.route('/users', methods=['GET'])
def users():
  current_user = get_user_by_username(session['user'])
  following_users = get_all_users_following(current_user[0])
  unfollowing_users = get_all_users_unfollowing(current_user[0])
  all_users = get_all_users()

  print('Not following: ', unfollowing_users)

  final_users = []
  for user in all_users:
    random_follow = random.choice([True, False])
    user = (user[0], user[1], user[2], random_follow)
    final_users.append(user)

  print(final_users)
  return render_template(
    'users_page.html',
    all_users=final_users,
    following_users=following_users,
    unfollowing_users=unfollowing_users,
  )


@app.route('/follow/<followee>')
def follow(followee):
  if 'user' not in session:
    return redirect(url_for('index'))

  current_user = get_user_by_username(session['user'])
  follow_user(current_user[0], followee)
  return redirect(url_for('users'))


app.run(host='0.0.0.0', port=81)
