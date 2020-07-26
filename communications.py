import os
import json
import tweepy
from BotBrain import BotBrain


class Communications:

    def __init__(self, cred_file):
        self.cred_file = cred_file
        self.api = None
        self.tweet = None

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
        self.tweet = bb.fetchQuote()

    def tweetIt(self):
        if self.tweet is not None:
            tweet = f"{self.tweet.text}\n-{self.tweet.author}"
            self.api.update_status(status=tweet)

    def main(self):
        credentials = self.loadCredentials()
        self.authenticate(credentials)
        self.getPost()
        self.tweetIt()


file = os.path.join(os.curdir, 'data', 'Twitter_Credential.json')
comm = Communications(file)
comm.main()

