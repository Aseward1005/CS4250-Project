import database_manager as database_manager
import rank as rank
import rankOrder as rankOrder
import indexing_utils as utils

def main():
    db = database_manager.connectDatabase()
    user_query = "deep learning"
    user_query_stopping = utils.remove_stop_words([user_query])
    vocabulary, vector_array, result_text = utils.stemming(user_query_stopping)

    matrix, prof, vocab = rank.rank(db.index, result_text[0])

    queryWeights = rankOrder.makeQueryWeights(result_text[0], vocab)


    
    print(rankOrder.rankResults(queryWeights, matrix, prof))


if __name__ == '__main__':
    main()