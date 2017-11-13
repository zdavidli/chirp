import tweepy
from tweepy.streaming import StreamListener
from tweepy import Stream
from config import *
import pdb
import json
from collections import Counter
import sqlite3

db = "../twit_data.db"
langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}


class twitter_listener(StreamListener):

    def __init__(self, num_tweets_to_grab, stats, get_tweet_html, retweet_count=10000, lang='en'):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.stats = stats
        self.get_tweet_html = get_tweet_html
        self.lang = lang

    def on_data(self, data):
        try:
            json_data = json.loads(data)

            if json_data["lang"] == self.lang:
                self.stats.add_lang(langs[json_data["lang"]])

                self.counter += 1
                retweet_count = json_data["retweeted_status"]["retweet_count"]

                if retweet_count >= self.retweet_count:
                    #print(json_data["text"], retweet_count, langs[json_data["lang"]])
                    self.stats.add_top_tweets(self.get_tweet_html(json_data['id']))
                    self.stats.add_top_lang(langs[json_data["lang"]])

                if self.counter >= self.num_tweets_to_grab:
                    return False

            return True
        except:
            # @TODO: Very dangerous, come back to this!
            pass

    def on_direct_message( self, status ):
        print("Entered on_direct_message()")
        try:
            print(status)
            return True
        except BaseException as e:
            print("Failed on_direct_message()", str(e))

    def on_error(self, status):
        print(status)

class TwitterMain():
    def __init__(self, num_tweets_to_grab, retweet_count, conn):
        self.auth = tweepy.OAuthHandler(cons_tok, cons_sec)
        self.auth.set_access_token(app_tok, app_sec)

        self.api = tweepy.API(self.auth)
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.stats = stats()
        self.conn = conn
        self.c = self.conn.cursor()


    def get_streaming_data(self):
        twitter_stream = Stream(self.auth, twitter_listener(num_tweets_to_grab=self.num_tweets_to_grab, retweet_count = self.retweet_count, stats = self.stats, get_tweet_html = self.get_tweet_html ))
        try:
            twitter_stream.sample()
        except Exception as e:
            print(e.__doc__)

        lang, top_lang, top_tweets = self.stats.get_stats()
        print(Counter(lang))
        print(Counter(top_lang))
        print(len(top_tweets))

        self.c.execute("INSERT INTO lang_data VALUES (?,?, DATETIME('now'))", (str(list(Counter(lang).items())), str(list(Counter(top_lang).items()))))

        for t in top_tweets:
            self.c.execute("INSERT INTO twit_data VALUES (?, DATETIME('now'))", (t,))

        self.conn.commit()

    def get_tweet_html(self, id):
        oembed = self.api.get_oembed(id=id, hide_media = True, hide_thread = True)

        tweet_html = oembed['html'].strip("\n")

        return tweet_html

class stats():

    def __init__(self):
        self.lang = []
        self.top_lang = []
        self.top_tweets = []

    def add_lang(self, lang):
        self.lang.append(lang)

    def add_top_lang(self, top_lang):
        self.top_lang.append(top_lang)

    def add_top_tweets(self, tweet_html):
        self.top_tweets.append(tweet_html)

    def get_stats(self):
        return self.lang, self.top_lang, self.top_tweets

if __name__ == "__main__":
    num_tweets_to_grab = 100
    retweet_count = 10000
    try:
        conn = sqlite3.connect(db)
        twit = TwitterMain(num_tweets_to_grab, retweet_count, conn)
        twit.get_streaming_data()


    except Exception as e:
        print(e.__doc__)

    finally:
        conn.close()
    #pdb.set_trace()

