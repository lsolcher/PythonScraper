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
    URL = 'http://www.spiegel.de/politik'
    SPON_PAGE = urlopen(URL)
    soup_mainpage = BeautifulSoup(SPON_PAGE, 'html.parser')
    
    # get all article URLs
    article_links = []
    for iteration in range(0, 10): 
        try:
            if iteration > 0:
                nextUrlTag = soup_mainpage.find('a', href=True, text='Mehr Artikel')
                URL ='http://www.spiegel.de' + nextUrlTag['href']
                SPON_PAGE = urlopen(URL)
                soup_mainpage = BeautifulSoup(SPON_PAGE, 'html.parser')
            for link in soup_mainpage.findAll('a', attrs={'href': re.compile("^(?!http://.*$).*")}):
                if '.html' in link['href'] and '-a-' in link['href']: #eliminate non-articles - SPON marks artikels with -a-
                    article_links.append('http://www.spiegel.de' + link['href'])
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
            thisArticle = []
            article_url = urlopen(article)
            soup_article = BeautifulSoup(article_url, 'html.parser')
            all_text = ''
            for text in soup_article.findAll('p'):
                all_text += text.getText()
            all_text = all_text.split('Wer steckt hinter Civey?')[0]
            all_text = all_text.split('© SPIEGEL ONLINE', 1)[0]
            all_text = all_text.replace('SPIEGEL ONLINE', 'SOURCE')
            fileId = 'articles\\SPON\\SPON_' + str(idx) + '.txt'
            fileName = os.path.join(dirpath, fileId)
            sponFile = open(fileName, 'w+', encoding='utf-8') 
            sponFile.write("%s\n" % all_text)
            sponFile.close
        except Exception:
            print(Exception)
            logger.exception("Error while parsing")
                
    
    

