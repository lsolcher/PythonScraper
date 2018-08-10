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
    logger.info('start scraping zeit')
    # Websites to scrape
    
    
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
    for link in soup_mainpage.findAll('a', attrs={'href': re.compile('^https://www.zeit.de/politik/')}):
        article_links.append(link['href'])
        logger.info('found recent article: ' + link['href'])
        
    article_links = list(set(article_links)) # eliminate duplicate entries
    zeitLinks = os.path.join(dirpath, "articleLinks\\zeitLinks.txt")
    
    
    linkFile = open(zeitLinks, 'w+')   
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
            all_text = all_text.split('Bitte melden Sie sich an, um zu kommentieren', 1)[0]
            all_text = all_text.replace('ZEIT ONLINE', 'SOURCE')
            fileId = 'articles\\ZEIT\\ZEIT_' + str(idx) + '.txt'
            fileName = os.path.join(dirpath, fileId)
            sponFile = open(fileName, 'w+', encoding='utf-8') 
            sponFile.write("%s\n" % all_text)
            sponFile.close
        except Exception:
            logger.exception("Error in parsing")    
    
    
    """
    article_links = []
    for iteration in range(0, 10): 
        try:
            if iteration > 0:
                nextUrlTag = soup_mainpage.find('a', href=True, text='Mehr Artikel')
                URL ='http://www.spiegel.de' + nextUrlTag['href']
                SPON_PAGE = urlopen(URL)
                soup_mainpage = BeautifulSoup(SPON_PAGE, 'html.parser')
            for link in soup_mainpage.findAll('a', attrs={'href': re.compile("^(?!http://.*$).*")}):
                if '.html' in link['href'] and '-a-' in link['href']: #eliminate non-articles
                    article_links.append('http://www.spiegel.de' + link['href'])
        except Exception:
            logger.exception("Error in fetching links")
    
    
    article_links = list(set(article_links)) # eliminate duplicate entries
    
    spon_links = os.path.join(dirpath, "sponLinks.txt") 
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
            for text in soup_article.findAll('p'):
                thisArticle.append(text.getText())
            fileId = 'articles\\SPON_' + str(idx) + '.txt'
            fileName = os.path.join(dirpath, fileId)
            sponFile = open(fileName, 'w+', encoding='utf-8') 
            sponFile.write("%s\n" % thisArticle)
            sponFile.close
        except Exception:
            logger.exception("Error in parsing")
                    
    """  
    

 