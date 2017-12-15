from twython import TwythonStreamer
import twitter_utils as utils
import config
import gevent

class TwitterStreamer(TwythonStreamer):

    def __init__(self, *args, **kwargs):
        TwythonStreamer.__init__(self, *args, **kwargs)
        print("Initialized TwitterStreamer.")
        self.queue = gevent.queue.Queue()

    def on_success(self, data):
        self.queue.put_nowait(data)
        if self.queue.qsize() > 10000:
            self.queue.get()

    def on_error(self, status_code, data):
        print(status_code, data, "TwitterStreamer stopped because of an error!")
        self.disconnect()

class TwitterWatchDog:
    def __init__(self, session):
        OAUTH_TOKEN = session['OAUTH_TOKEN']
        OAUTH_TOKEN_SECRET = session['OAUTH_TOKEN_SECRET']
        self.streamer = TwitterStreamer(config.CONSUMER_KEY, config.CONSUMER_SECRET,
                                        OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.green = gevent.spawn(self.streamer.statuses.filter)

    def check_alive(self):
        if self.green.dead:
            self.streamer.disconnect()
            self.green.kill()
            self.__init__()

