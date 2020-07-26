import requests
import os
from bs4 import BeautifulSoup
from random import randint


class QuoteFetcher:

    def __init__(self, work_dir=os.curdir, scrape_link=None, topic="life"):
        self.work_dir = work_dir
        self.url_list = []
        self.fetch_topic = topic
        if scrape_link is None:
            self.scrape_link = "https://www.brainyquote.com"
        else:
            self.scrape_link = scrape_link


    def createConnection(self):
        url = f'{self.scrape_link}/topics/{self.fetch_topic}-quotes'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        class_list = soup.findAll('div', {'class': "clearfix"})
        self.url_list = [a.a['href'] for a in class_list]
        return self

    def url_count(self):
        return len(self.url_list)

    def getRandomUrl(self):
        q_idx = randint(0, len(self.url_list)-1)
        q_url = self.scrape_link + self.url_list[q_idx]
        return q_url

    def setTopic(self, topic):
        self.fetch_topic = topic

    def getQuoteText(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        quote = soup.find('div', {'class': 'quoteContent'}).text
        quote = [text for text in quote.split('\n') if text != '']
        idx = soup.findAll('p')[0]['class'][1]
        result = [idx] + quote
        return result

    def getQuoteImage(self, url):
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
