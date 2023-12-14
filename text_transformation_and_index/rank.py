import database_manager as database_manager

import indexing_utils as utils
import rankOrder as rankOrder

def rank(dbHandle, text):

    '''
    Vectorize Text
    '''
    # Remove Stop Words
    text = utils.remove_stop_words([text])

    # Perform Stemming
    vocabulary, vector_array, result_text = utils.stemming(text)
    
    '''
    Query Database for related tf-idfs

    For each term store [(professorName, tf-idf), ... ]
    '''
    # Figure out how many terms there are
    termSize = len(vocabulary.keys())

    # Professor -> [Array of TF IDF Values]
    tf_idf_table = {}
    
    # Keep track of the term and the index so we know
    # where to store tf_idf in the array
    for term, term_pos in vocabulary.items():

        # PyMongo Query
        query = {'Term': term}
        results = database_manager.get_index(dbHandle, query)

        # Pymongo Formatting Requires This
        for res in results:

            # For Each Professor In the Results
            for prof in res['Documents']:

                # Extracted Info We Need
                name = prof['Professor Name']
                tf_idf = prof['tf_idf']

                # Get the Array For That Professor
                # If the array hasn't been created yet
                # Create an array that is the size of the
                # number of terms
                data = tf_idf_table.get(name, [0]*termSize)
                data[term_pos] = tf_idf

                tf_idf_table[name] = data


    # Transform the Dictionary into A Matrix Format
    tf_idf_matrix = []
    professors  = []
    for professor, tf_idf_array in tf_idf_table.items():
        tf_idf_matrix.append(tf_idf_array)
        professors.append(professor)

    '''
        tf_idf_matrix - Matrix storing TF IDF Valuess
        professors - Array which contains professor names.
                     Correlate this index with the specific
                     row in the matrix
        vocabulary - Dictionary specifying the specific terms
                     in the tf_idf table. The Key is the term,
                     the value is the column in the matrix.
    '''
    return tf_idf_matrix, professors, vocabulary
    
def query(user_query):
    db = database_manager.connectDatabase()

    user_query_stopping = utils.remove_stop_words([user_query])
    vocabulary, vector_array, result_text = utils.stemming(user_query_stopping)

    matrix, prof, vocab = rank(db.index, result_text[0])

    queryWeights = rankOrder.makeQueryWeights(result_text[0], vocab)

    results = rankOrder.rankResults(queryWeights, matrix, prof)
    return results


def main():
    res = query("deep learning")

    print(res)


if __name__ == '__main__':
    main()