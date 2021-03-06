# -*- coding: utf-8 -*-
"""
Created on Sat May 26 18:09:57 2018

@author: Luc
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import logging
import os.path


def scrape(dirpath):
    logger = logging.getLogger('root')
    logger.info('start scraping junge freiheit')

    # Websites to scrape
    URL = []
    URL.append('https://jungefreiheit.de/kategorie/politik/')
    URL.append('https://jungefreiheit.de/kategorie/wirtschaft/')
    URL.append('https://jungefreiheit.de/kategorie/kultur/')
    URL.append('https://jungefreiheit.de/kategorie/wissen/')
    URL.append('https://jungefreiheit.de/kategorie/debatte/')
    PAGE = []
    for url in URL:
        PAGE.append(urlopen(url))
    soup_mainpages = []
    for page in PAGE:
        soup_mainpages.append(BeautifulSoup(page, 'html.parser'))

    # get all article URLs
    article_links = set()
    for i, category in enumerate(soup_mainpages):
        for iteration in range(0, 100):
            try:
                if iteration > 0:
                    nextUrlTag = category.find('a', href=True, text=re.compile('Nächste Seite'))
                    URL[i] = nextUrlTag['href']
                    PAGE[i] = urlopen(URL[i])
                    category = BeautifulSoup(PAGE[i], 'html.parser')
                for link in category.findAll('a', attrs={'href': re.compile("^https://jungefreiheit.de/.*")}):
                    if link['href'] and '2018' in link['href'] and '/#comments' not in link['href']:  # eliminate non-articles
                        article_links.add(link['href'])
                        if len(article_links) % 100 == 0:
                            print('Fetching articles. Found {} unique articles so far.'.format(len(article_links)))
            except TypeError:
                logger.exception('Done with category {}. Moving to the next one.'.format(i))
                range = 100
                i += 1
            except Exception:
                logger.exception("Error while fetching links")

    article_links = list(set(article_links))  # eliminate duplicate entries
    print('Found {} unique articles in total. Start writing...'.format(len(article_links)))
    links = os.path.join(dirpath, "articleLinks\\jfLinks.txt")
    linkFile = open(links, 'w+')
    for link in article_links:
        linkFile.write("%s\n" % link)

    # get article text and save it to file
    print(len(article_links))
    for idx, article in enumerate(article_links):
        try:
            if idx % 100 == 0:
                print('Wrote {} of {} articles.'.format(idx, len(article_links)))
            article_url = urlopen(article)
            soup_article = BeautifulSoup(article_url, 'html.parser')
            article = soup_article.find("div", {"class": "entry-content"}).findAll('p')
            text = ''
            for idy, element in enumerate(article):
                if idy < len(article) - 1 and idy != 0: # remove press agency parentheses and header
                    text += ''.join(element.findAll(text=True))
            text = re.sub(r"\b[A-Z]+(?:\s+[A-Z]+)*\b. ", '', text)  # remove uppercased city
            fileId = 'articles\\JF\\JF_' + str(idx) + '.txt'
            fileName = os.path.join(dirpath, fileId)
            sponFile = open(fileName, 'w+', encoding='utf-8')
            sponFile.write("%s\n" % text)
            sponFile.close
        except Exception:
            print(Exception)
            logger.exception("Error while parsing")




