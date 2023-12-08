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
    
    #Finds the name of the professor
    name = bs.find_all("title")

    #Finds the accolade sidebar and determines which sections need to be saved by looking for header text
    #Saves data in variable 'research_text'
    accolades = bs.find_all('div', {'class': 'accolades'})
    for accolade in accolades:
        if accolade.find('h2', string=re.compile(r"^R")):
            bs.find('h2', string=re.compile(r"^R")).decompose()
            research_text = accolade.text
        elif bs.find('h2', string=re.compile(r"^Publications")):
            bs.find('h2', string=re.compile(r"^Publications")).decompose()
            research_text = accolade.text
        else:
            continue

    #MongoDB connection
    client = MongoClient('mongodb://localhost:27017/')
    db = client['cs4250project']
    collection = db['professors']

    #Upsert MongoDB data
    collection.insert_one({"name": name[0].text, "research": research_text})
    client.close()

#Insert website of choice here:
find_research("https://www.cpp.edu/faculty/yongpingz/")

