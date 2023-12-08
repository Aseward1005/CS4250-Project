from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymongo
import re

def crawlerThread(frontier, target, col):
    for site in frontier:
        print(site)
        base = re.match('https://\w*\.\w+\.\w+', site).group()
        #print(base)
        html = urlopen(site).read()
        storePage(site, html, col)
        bs = BeautifulSoup(html, 'html.parser')
        #relative_links = bs.find_all('a', {'href': re.compile('^/.*')})
        #print([link.get('href') for link in relative_links])
        #print('\n')
        #absolute_links = bs.find_all('a', {'href': re.compile('^https://.*')})
        #print([link.get('href') for link in absolute_links])
        #print('\n')
        links = bs.find_all('a', {'href': re.compile('/')})
        #print([link.get('href') for link in links])
        urls = [link.get('href') for link in links]
        #print('\n')
        #append start to relative links
        for i,url in enumerate(urls):
            if (url.startswith('/')):
                urls[i] = base + url
        #print(urls)

        for url in urls:
            if url not in frontier:
                frontier.append(url)

        if (site == target):
            break #i hate break statements and if I wasn't super busy i would refactor this entire thing

def storePage(url, html, col):
    doc = {'url': url,
           'html': str(html)}
    
    col.insert_one(doc)


def main():
    seed = 'https://www.cpp.edu/sci/computer-science/'
    frontier = [seed]

    target = 'https://www.cpp.edu/sci/computer-science/faculty-and-staff/permanent-faculty.shtml'

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.corpus
    pages = db.pages

    crawlerThread(frontier, target, pages)

    print('done')

if __name__ == '__main__':
    main()