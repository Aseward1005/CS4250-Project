import text_transformation_and_index.indexing_utils
import text_transformation_and_index.database_manager
import text_transformation_and_index.rank
from sklearn.metrics.pairwise import cosine_similarity

import math

def makeQueryWeights(vocab):
    queryWeight = {}
    for term, index in vocab:
        tf = 1/len(vocab)
        df = 1
        idf = math.log2(1/df)
        tf_idf = tf * idf
        queryWeight.update({index: tf_idf})
    return queryWeight

#quicksort helper method that works for dictionaries
def quicksort_dict(input_dict):
    if len(input_dict) <= 1:
        return input_dict
    else:
        pivot_key = next(iter(input_dict))
        pivot_value = input_dict[pivot_key]
        
        less = {k: v for k, v in input_dict.items() if v <= pivot_value and k != pivot_key}
        greater = {k: v for k, v in input_dict.items() if v > pivot_value}

        return {**quicksort_dict(less), pivot_key: pivot_value, **quicksort_dict(greater)}
    
def rankResults(queryWeights, matrix, prof):
    sorted_dict = {}
    for index, row in enumerate(matrix):
        query = queryWeights[index]
        sorted_dict.update({prof[index], cosine_similarity(query, row[index])})
    return quicksort_dict(sorted_dict)
        


            
            
            
            
    

