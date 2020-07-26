from QuoteFetcher import QuoteFetcher
import os
from random import randint


class Quote:

    def __init__(self, topic=""):
        self.text = ""
        self.image_link = ""
        self.topic = topic
        self.url = ""
        self.idx = ""
        self.author = ""

    def __str__(self):
        return f'{self.text} - {self.author}'


class BotBrain:

    def __init__(self, data_dir=None, base_link=None):
        if data_dir is None:
            self.data_dir = os.path.join(os.curdir, 'data')
        else:
            self.data_dir = data_dir
        self.base_link = base_link

    def getRandomTopic(self):
        topic_list = open(os.path.join(self.data_dir, 'topics.txt')).read().split(',')
        topic = topic_list[randint(0, len(topic_list)-1)]
        return topic

    def fetchQuote(self):
        qf = QuoteFetcher(self.data_dir, self.base_link)
        topic = self.getRandomTopic()
        qf.setTopic(topic)
        qf.createConnection()
        quote = Quote(topic)
        quote.url = qf.getRandomUrl()
        quote.idx, quote.text, quote.author = qf.getQuoteText(quote.url)
        try:
            quote.image_link = qf.getQuoteImage(quote.url)
        except TypeError:
            quote.image_link = None
        self.saveResults(quote)
        return quote

    def changeTopic(self, qf, topic):
        qf.setTopic(topic)

    def saveResults(self, quote):
        file_path = os.path.join(self.data_dir, 'quote_dump.csv')
        with open(file_path, 'a') as dump_file:
            dump_file.write(f"{quote.idx}|{quote.topic}|{quote.text}|{quote.author}|{quote.image_link}\n")
