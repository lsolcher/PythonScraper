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
import string


def scrape(dirpath):
    logger = logging.getLogger('root')
    logger.info('start scraping spon')

    # Websites to scrape
    URL = []
    URL.append('http://www.spiegel.de/politik/')
    URL.append('http://www.spiegel.de/thema/meinung/')
    URL.append('http://www.spiegel.de/wirtschaft/')
    URL.append('http://www.spiegel.de/panorama/')
    URL.append('http://www.spiegel.de/kultur/')
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
                    nextUrlTag = category.find('a', href=True, text='Mehr Artikel')
                    URL[i] = 'http://www.spiegel.de'+ nextUrlTag['href']
                    PAGE[i] = urlopen(URL[i])
                    category = BeautifulSoup(PAGE[i], 'html.parser')
                for link in category.findAll('a', attrs={'href': re.compile("^(?!http://.*$).*")}):
                    if '.html' in link['href'] and '-a-' in link['href'] and '/plus/' not in link['href'] \
                            and 'news-' not in link['href']: #eliminate non-articles - SPON marks artikels with -a-
                        article_links.add('http://www.spiegel.de' + link['href'])
                        if len(article_links) % 100 == 0:
                            print('Fetching articles. Found {} unique articles so far.'.format(len(article_links)))

            except TypeError:
                logger.exception('Done with category {}. Moving to the next one.'.format(i))
                i += 1

            except Exception:
                logger.exception("Error while fetching links")
    
    
    article_links = list(set(article_links)) # eliminate duplicate entries
    
    spon_links = os.path.join(dirpath, "articleLinks\\sponLinks.txt") 
    linkFile = open(spon_links, 'w+')   
    for link in article_links:
        linkFile.write("%s\n" % link)
        
        
    # get article text and save it to file
    print(len(article_links))
    for idx, article in enumerate(article_links):
        try:
            article_url = urlopen(article)
            soup_article = BeautifulSoup(article_url, 'html.parser')
            all_text = ''
            for text in soup_article.findAll('p'):
                all_text += text.getText()
            all_text = all_text.split('Wer steckt hinter Civey?', 1)[0]
            all_text = all_text.split('© SPIEGEL ONLINE', 1)[0]
            all_text = all_text.replace('SPIEGEL ONLINE', '')
            all_text = all_text.replace('SPIEGEL+', '')
            all_text = all_text.replace('SPIEGEL', '')
            if all_text:
                fileId = 'articles\\SPON\\SPON_' + str(idx) + '.txt'
                fileName = os.path.join(dirpath, fileId)
                sponFile = open(fileName, 'w+', encoding='utf-8')
                sponFile.write("%s\n" % all_text)
                sponFile.close
        except Exception:
            print(Exception)
            logger.exception("Error while parsing")
                
    
    

