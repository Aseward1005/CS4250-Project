from bs4 import BeautifulSoup
import pymongo
import re

#getting the html from the url
def getDict(source, target):
    return source.find_one({'title':target})

#focusing the parser to where the professors are located
def getFacultyTags(html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find('div', {'class':'row justify-content-left'}).find_all('div', {'class': 'col-md directory-listing'})
    
#parsing and storing in mongodb
def storeInfo(html, dest):
    #name and title are outside the ul tag (where everything else is stored)
    #we handle those first
    name = html.find('h3')
    title = html.find('div', {'class': 'mb-1 text-muted'})

    #incase there's a blank card
    if name is None:
        return
    
    #formatting
    name = name.get_text().replace("\\n", '').strip()
    title = title.get_text().strip()

    #parse the rest of the card for its data, put it all in a dictionary
    info = getInfo(html)
    info['name'] = name
    info['title'] = title
    print(info)

    #insert the data to mongodb
    dest.insert_one(info)

def getInfo(html):
    infoHtml = html.find('ul')
    result = {}

    #all our info is within span tags
    #the field its storing is in the text, the data is the next sibling
    fields = infoHtml.find_all('span')
    
    #get the website, which is slightly different from the rest but it's at the end
    result['website'] = fields.pop().get_text().strip() #his is wrong because sid is dumb
    result['website'] = infoHtml.find_all('a').pop()['href'].strip()

    #get the rest of the data using the scheme listed above
    for field in fields:
        result[field.get_text()] = field.next_sibling

    return result


def main():
    target = 'Faculty and Staff'

    #database connection
    client = pymongo.MongoClient(host='localhost', port=27017)
    db = client.cs4250project
    pages = db.pages
    professors = db.professors
    
    #getting data to parse
    html = getDict(pages, target)['html']
    profs = getFacultyTags(html)

    #actual parsing and storing
    for prof in profs:
        storeInfo(prof, professors)
        print('\n')

if __name__ == '__main__':
    main()
    print('done')