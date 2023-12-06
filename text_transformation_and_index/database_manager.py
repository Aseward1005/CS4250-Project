from pymongo import MongoClient

def connectDatabase():
    DB_NAME = "cs4250project"
    DB_HOST = "localhost"
    DB_PORT = 27017

    try:
        client = MongoClient(host=DB_HOST, port=DB_PORT)
        db = client[DB_NAME]
        return db
    except:
        print("Database not connected succesfully.")


def get_professor_research_blob(col):
    return col.find({},{\
        "_id": 0,
        "name": 1,
        "research": 1,
    })
    
def insertDocument(col, key, document):
    print(key)
    print(document)
    col.update_one(key, document, upsert=True)

def update_index(col, term, professorName, frequency):
    key = {"Term" : term}
    newDocument = {
        "Professor Name" : professorName,
        "Frequency" : frequency.item()
    }
    
    operation = {"$push" : {"Documents" : newDocument}}

    insertDocument(col, key, operation)