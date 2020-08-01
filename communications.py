import os
import json
import tweepy
from BotBrain import BotBrain


class twiiterConnect:

    def __init__(self, cred_file):
        self.cred_file = cred_file
        self.api = None
        self.quote_tweet = None
        self.joke_tweet = None

    def loadCredentials(self):
        with open(self.cred_file, 'r') as file:
            credentials = json.load(file)
        return credentials

    def authenticate(self, credentials):
        auth = tweepy.OAuthHandler(
            credentials['CONSUMER_KEY'],
            credentials['CONSUMER_SEC']
        )

        auth.set_access_token(
            credentials['ACCESS_TOKEN'],
            credentials['ACCESS_SEC']
        )
        self.api = tweepy.API(auth)

    def getPost(self):
        bb = BotBrain()
        self.quote_tweet = bb.fetchQuote()
        self.joke_tweet = bb.fetchJoke()


    def tweetIt(self):
        if self.quote_tweet is not None:
            quote_tweet = f"{self.quote_tweet.text}\n-{self.quote_tweet.author}\n#Quotes #{self.quote_tweet.topic}"
            self.api.update_status(status=quote_tweet)

    def tweetJoke(self):
        if self.joke_tweet is not None:
            joke_tweet = f"{self.joke_tweet}"
            self.api.update_status(status=joke_tweet)

    def main(self):
        #credentials = self.loadCredentials()
        #self.authenticate(credentials)
        self.getPost()
        #self.tweetIt()
        self.tweetJoke()


file = os.path.join(os.curdir, 'data', 'Twitter_Credential.json')
comm = twiiterConnect(file)
comm.main()

