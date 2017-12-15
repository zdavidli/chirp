from twython import Twython
import config

def auth_session(session):
    assert('OAUTH_TOKEN' in session.keys())
    assert('OAUTH_TOKEN_SECRET' in session.keys())
    OAUTH_TOKEN = session['OAUTH_TOKEN']
    OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
    twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    return twitter

def init_session(callback='http://localhost:5000/login'):
    twitter = Twython(config.CONSUMER_KEY, config.CONSUMER_SECRET)
    auth = twitter.get_authentication_tokens(callback_url=callback)

    return twitter, auth
