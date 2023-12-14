from sklearn.feature_extraction.text import CountVectorizer
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import math

import database_manager

class LemmaTokenizer:
      def __init__(self):
          self.wnl = WordNetLemmatizer()
      def __call__(self, doc):
          return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def remove_stop_words(text):
    vectorizer = CountVectorizer(stop_words='english')
    print(vectorizer.stop_words)

    vectorizer.fit(text)
    # Represents the Index of each term
    vocab = vectorizer.vocabulary_

    vector = vectorizer.transform(text)
    # Represents the count of each term where the index above describes the termsssssss
    vector_array = vector.toarray()

    # Remove Stopping Words from text
    # Side Effect - Will Reformat order of text
    results = []
    for v in vector_array:
        results.append(form_new_text(vocab, v))
    
    return results

def stemming(text):
    vectorizer = CountVectorizer(tokenizer=LemmaTokenizer())
    vectorizer.fit(text)
    vocab = vectorizer.vocabulary_
    vector = vectorizer.transform(text)
    vector_array = vector.toarray()
    results = []
    for v in vector_array:
        results.append(form_new_text(vocab, v))
    
    return vocab, vector_array, results

def index(databaseHandler, professor_names, vocab, vector_array):
    professor_document_size = []
    document_frequency = [None] * len(vocab)
    for vector in vector_array:
        professor_document_size.append( sum(vector) )

    for token, index in vocab.items():
        for i, prof_name in enumerate(professor_names):
            if vector_array[i][index] != 0:
                if document_frequency[index] == None:
                    document_frequency[index] = document_frequency_calculation(vector_array, index)
                    
                tf = vector_array[i][index] / professor_document_size[i]
                df = document_frequency[index]
                idf = math.log( len(professor_document_size) / df )
                tf_idf = tf * idf

                database_manager.update_index(databaseHandler, token, prof_name, vector_array[i][index], tf_idf)

    print("Finished")

def form_new_text(dictonary, token_vector):
    resulting_text = []
    for token, index in dictonary.items():
        if token_vector[index] != 0:
            for _ in range(token_vector[index]):
                resulting_text.append(token)
    return " ".join(resulting_text)

def document_frequency_calculation(vector_array, index):
    sum = 0
    for vector in vector_array:
        if vector[index] > 0:
            sum += 1
    return sum
