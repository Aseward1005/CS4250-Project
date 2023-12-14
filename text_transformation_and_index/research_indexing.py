import database_manager
import indexing_utils

def getProfessorData(databaseHandler):
    return database_manager.get_professor_research_blob(databaseHandler)

def indexData(databaseHandler, professorData):
    professorNames, researchBlobs = [], []
    for professor in professorData:
        if professor['research'] is not None:
            professorNames.append(professor['name'])
            researchBlobs.append(professor['research'])

    # Perform Text Transformation
    researchBlobs.append("Trees Tree")
    researchBlobs = indexing_utils.remove_stop_words(researchBlobs)
    vocab, vector_array, researchBlobs = indexing_utils.stemming(researchBlobs)

    # Find all Indexes
    # Return a Dictionary of All The Terms {'Term': Term Frequency}
    tokens = indexing_utils.index(databaseHandler, professorNames, vocab, vector_array)

    return 1

def main():
    print("Running indexing...")
    database = database_manager.connectDatabase()

    professor_data = getProfessorData(database.professors)
    
    database.index.drop()
    res = indexData(database.index, professor_data)

    if res == 1:
        print("Finished Successfully")

if __name__ == "__main__":
    main()