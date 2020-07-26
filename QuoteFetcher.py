import requests
import os
from bs4 import BeautifulSoup
from random import randint


""" Author : Akash Agnihotri <akashagni26@gmail.com>
    Created Date : 25th July 2020
    Overview : This class provides API to scrape Quote's website to fetch quotes.
    Latest Change : Created
"""


class QuoteFetcher:

    def __init__(self, work_dir=os.curdir, scrape_link=None, topic="life"):
        """
        This class provides functionality to scrape the internet for quotes
        :param work_dir: provide work directory, where all new quotes will be saved, and list of topics will be fetched.
        :param scrape_link:  Base link from where to search the quotes,default is https://www.brainyquote.com
        :param topic: Topic on which to search the quotes, default is life
        """
        self.work_dir = work_dir
        self.url_list = []
        self.fetch_topic = topic
        if scrape_link is None:
            self.scrape_link = "https://www.brainyquote.com"
        else:
            self.scrape_link = scrape_link


    def createConnection(self):
        """
        Create as connection to the scrape link and fetches a list of quotes link related to mentioned topic.
        :return: self
        """
        url = f'{self.scrape_link}/topics/{self.fetch_topic}-quotes'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        class_list = soup.findAll('div', {'class': "clearfix"})
        self.url_list = [a.a['href'] for a in class_list]
        return self

    def url_count(self):
        """
        Returns count of URL's found in search
        :return: int
        """
        return len(self.url_list)

    def getRandomUrl(self):
        """
        returns a random URL link from the scraped page
        :return: string
        """
        q_idx = randint(0, len(self.url_list)-1)
        q_url = self.scrape_link + self.url_list[q_idx]
        return q_url

    def setTopic(self, topic):
        """
        Set the topic parameter to a new value
        :param topic: Set to any available topic
        :return: None
        """
        self.fetch_topic = topic

    def getQuoteText(self, url):
        """
        Fetches the Text from the Quote of the link provided.
        :param url: Url from which to get the quote
        :return: String
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        quote = soup.find('div', {'class': 'quoteContent'}).text
        quote = [text for text in quote.split('\n') if text != '']
        idx = soup.findAll('p')[0]['class'][1]
        result = [idx] + quote
        return result

    def getQuoteImage(self, url):
        """
        Fetches the Image from the quote
        :param url: url from which t fetch the quote
        :return: String
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find('div', {'class': 'quoteContent'})
        q_img_link = content.a.img['data-img-url']
        q_img_link = self.scrape_link + q_img_link
        idx = soup.findAll('p')[0]['class'][1]
        q_img = requests.get(q_img_link)
        file_name = idx + '.jpg'
        full_file_path = os.path.join(self.work_dir, 'images', file_name)
        img_file = open(full_file_path, 'wb')
        img_file.write(q_img.content)
        img_file.close()
        return full_file_path

    def main(self):
        """
        For Testing the class
        :return: None
        """
        topic_list = open(os.path.join(self.work_dir, 'data', 'topics.txt')).read().split(',')
        topic = topic_list[randint(0, len(topic_list))]
        self.fetch_topic = topic
        self.createConnection()
        q_idx = randint(0, len(self.url_list))
        q_url = self.scrape_link + self.url_list[q_idx]
        q_text = self.getQuoteText(q_url)
        print(q_text)
        try:
            q_img = self.getQuoteImage(q_url)
            print(q_img)
        except TypeError:
            print('Image Not Available')
