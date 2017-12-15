from twython import Twython
import json
import twitter_utils as utils

def login_button(callback='http://localhost:5000/login'):
    return utils.init_session(callback)

def first_login(session, oauth_verifier):
    twitter = utils.auth_session(session)
    final_step = twitter.get_authorized_tokens(oauth_verifier)
    session['OAUTH_TOKEN'] = final_step['oauth_token']
    session['OAUTH_TOKEN_SECRET'] = final_step['oauth_token_secret']
    return twitter, session

def login(session):
    return utils.auth_session(session)
