# Install required packages
## Make sure you are using python 3.8+
```
python3 -m venv venv
source venv/bin/active
pip install poetry
poetry install
```

# Run the app
```
flask --app main run --port 8000
```

Users
==========
_id    username
1        raptor
2        paul

Tweets
==========
_id  user_id    tweet
1    1        Helo how are you?
2    2        My name is Paul


Likes
=============
user_id    tweet_id
1            2
2            1


In the view we need:
===================
Authenticated user: Paul

Paul sees the following in the /tweets page

user        tweet                liked by authenticated user?
raptor    Hello how are you?         yes/no   -> like/unlike