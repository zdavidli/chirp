# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '924672510607740928-jDI8M1Jj2tJI9WIPSlkecXFxPbpUQzq'
ACCESS_SECRET = '8SFcadeAvsDDiCnpsorU4CSeF0PSfRcrEYKe9rpPapwhs'
CONSUMER_KEY = 'XCdXvVlN5DTjuU2FHaIngLK75'
CONSUMER_SECRET = 'Gish3f1JVQkPWWFZRtzfVUhFNzTRnrnq7qlcu23sV07awSoiRR'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)
            
# Search for latest tweets about "#nlproc"
a = twitter.search.tweets(q='#Twitter4Me')

print json.dumps(a)