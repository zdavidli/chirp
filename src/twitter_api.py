from twython import Twython
import json
import twitter_utils as utils

def get_messages(count, session):
    try:
        twitter = utils.auth_session(session)
        response = twitter.get_direct_messages(count=count)
        if response:
            response = json.dumps(response)
            return response, 200
        else:
            return "Error retrieving messages", 500
    except AssertionError:
        return "Error in authentication", 500


def get_feed(count, session):
    try:
        twitter = utils.auth_session(session)
        response = twitter.get_home_timeline(count=count)
        if response:
            response = json.dumps(response)
            return response, 200
        else:
            return "Error retrieving tweets", 500
    except AssertionError:
        return "Error in authentication", 500

def get_user_id(session):
    try:
        twitter = utils.auth_session(session)
        response = twitter.get("account/verify_credentials")
        user_id = response[u"id_str"]
        if user_id:
            return str(user_id), 200
        else:
            return 'Error retrieving user_id', 500
    except AssertionError:
        return "Error in authentication", 500
