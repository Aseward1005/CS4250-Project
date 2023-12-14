from sklearn.metrics.pairwise import cosine_similarity

import math

def makeQueryWeights(string, vocab):
    query_weights = [0] * len(vocab.keys())
    for word in string.split():
        query_weights[ vocab[word] ] = query_weights[ vocab[word] ] + 1
    
    for i in range(len(query_weights)):
        query_weights[i] = query_weights[i]/ len(string.split())

    return query_weights


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
        cosine_sim = cosine_similarity([queryWeights], [row])
        sorted_dict.update({prof[index]: cosine_sim})
    return quicksort_dict(sorted_dict)
        


            
            
            
            
    

