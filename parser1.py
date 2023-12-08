from bs4 import BeautifulSoup
import pymongo
import re

def getDict(source, target):
    return source.find_one({'title':target})

def getFacultyTags(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'class':'row justify-content-left'}).find_all('div', {'class': 'col-md directory-listing'})
    
def storeInfo(html, dest):
    name = html.find('h3')
    title = html.find('div', {'class': 'mb-1 text-muted'})

    if name is None:
        return
    
    name = name.get_text().replace("\\n", '').strip()
    title = title.get_text().strip()
    info = getInfo(html)
    info['name'] = name
    info['title'] = title
    print(info)

    dest.insert_one(info)

def getInfo(html):
    infoHtml = html.find('ul')
    result = {}

    fields = infoHtml.find_all('span')
    
    #get the website
    result['website'] = fields.pop().get_text().strip()

    for field in fields:
        result[field.get_text()] = field.next_sibling
    #1 is office
    #result['office'] = fields[1].next_sibling.replace(':', '')
    #print(office)
    #2 is phone, which was not asked for

    #fields = infoHtml.find_all('a')
    #print([field.get_text() for field in fields])
    #0 is email
    #result['email'] = fields[0].get_text()
    #print(email)
    #1 is website
    #result['website'] = fields[1].get_text()
    #print(website)

    return result


def main():
    target = 'Faculty and Staff'

    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.cs4250project
    pages = db.pages
    professors = db.professors
    
    html = getDict(pages, target)['html']
    profs = getFacultyTags(html)

    print('\n')
    for prof in profs:
        storeInfo(prof, professors)

if __name__ == '__main__':
    main()
    print('done')