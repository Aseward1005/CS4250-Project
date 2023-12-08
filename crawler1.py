from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymongo
import re

def FindTargetPage(frontier, targetTitle, col):
    for site in frontier:
        print(site)
        base = re.match('https://\w*\.\w+\.\w+', site).group()
        
        html = urlopen(site).read()
        bs = BeautifulSoup(html, 'html.parser')
        title = bs.find('title').getText().strip()
        storePage(title, site, html, col)

        #find the links
        links = bs.find_all('a', {'href': re.compile('/')})
        urls = [link.get('href') for link in links]

        #append start to relative links
        for i,url in enumerate(urls):
            if (url.startswith('/')):
                urls[i] = base + url

        for url in urls:
            if url not in frontier:
                frontier.append(url)

        if (title == targetTitle):
            break #i hate break statements and if I wasn't super busy i would refactor this entire thing

def storePage(title, url, html, col):
    doc = {'title': title,
           'url': url,
           'html': str(html)}
    
    col.insert_one(doc)


def main():
    seed = 'https://www.cpp.edu/engineering/ce/index.shtml'
    frontier = [seed]

    target = 'Faculty and Staff'

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.cs4250project
    pages = db.pages

    FindTargetPage(frontier, target, pages)

    print('done')

if __name__ == '__main__':
    main()