from urllib.request import urlopen
from pymongo import MongoClient
from bs4 import BeautifulSoup
import re

#Crawls a webpage and inserts the professor's name from the title as well as their research interests into MongoDB
def find_research(url):

    #Opens url and inits BeautifulSoup
    html = urlopen(url)
    page = html.read()
    bs = BeautifulSoup(page, 'html.parser')

    #Finds the accolade sidebar and determines which sections need to be saved by looking for header text
    #Saves data in variable 'research_text'
    research_text = None
    accolades = bs.find_all('div', {'class': 'accolades'})
    for accolade in accolades:
        if accolade.find('h2', string=re.compile(r"^R")):
            bs.find('h2', string=re.compile(r"^R")).decompose()
            research_text = accolade.text
            break
        elif bs.find('h2', string=re.compile(r"^Publications")):
            bs.find('h2', string=re.compile(r"^Publications")).decompose()
            research_text = accolade.text
            break
        else:
            continue

    return research_text

def main():
    #MongoDB connection
    client = MongoClient(host='localhost', port=27017)
    db = client['cs4250project']
    collection = db['professors']

    for professor in collection.find():
        collection.update_one({"_id": professor["_id"]}, {"$set": {"research" : find_research(professor['website'])}})

    client.close()


if __name__ == '__main__':
    main()