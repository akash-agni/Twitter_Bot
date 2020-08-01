import requests
import os
from bs4 import BeautifulSoup
from random import randint

""" Author : Akash Burnwal <akashburnwal005@gmail.com>
    Created Date : 25th July 2020
    Overview : This class provides API to scrape jokes website to fetch jokes based on topics.
    Latest Change : Created
"""


class JokeFetcher:

    def __init__(self, work_dir=os.curdir, scrape_link=None, topic="one-liner"):
        """
        This class provides functionality to scrape the internet for jokes
        :param work_dir: provide work directory, where all new quotes will be saved, and list of topics will be fetched.
        :param scrape_link:  Base link from where to search the quotes,default is https://www.jokes.lol
        :param topic: Topic on which to search the jokes, default is one-liner
        """
        self.work_dir = work_dir
        #self.url_list = []
        self.fetch_topic = topic
        if scrape_link is None:
            self.scrape_link = "https://jokes.lol/"
        else:
            self.scrape_link = scrape_link
        self.soup = None
        


    def createConnection(self):
        """
        Create as connection to the scrape link and fetches html link related to mentioned topic of any page.
        :return: self
        """
        random_page = randint(1,9)
        url = f'{self.scrape_link}/{self.fetch_topic}-jokes/page/{random_page}'
        print(url)
        page = requests.get(url)
        self.soup = BeautifulSoup(page.content, 'html.parser')

    def setJokeTopic(self, topic):
        """
        Set the topic parameter to a new value
        :param topic: Set to any available topic
        :return: None
        """
        self.fetch_topic = topic

    def getJokeText(self):
        """
        Fetches the Text from any random joke of the page.
        :param soup: HTML code from the jokes page
        :return: String
        """
        jokes_in_page = self.soup.findAll('div',{'class':'entry-content clear'})
        total_jokes = len(jokes_in_page)
        ran_joke = jokes_in_page[randint(0,total_jokes-1)].text.replace('ShareTweet','').strip()
        return ran_joke

    def main(self):
        """
        For Testing the class
        :return: None
        """
        topic_list = open(os.path.join(self.work_dir, 'data', 'joke_topics.txt')).read().split('\n')
        joke_topic = topic_list[randint(0, len(topic_list)-1)]
        self.fetch_topic = joke_topic
        self.createConnection()
        joke = self.getJokeText()
        print(joke)