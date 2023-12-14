import indexing_utils as utils
import rankOrder as rankOrder
import database_manager as database_manager
import rank as rank
import math

# search engine interface

def search_engine(search_query):
    # return results ranked
    
    db = database_manager.connectDatabase()
    professor_names = list(rank.query(search_query))
    
    result_urls = []
    
    for prof_name in professor_names:
        prof_doc = db.professors.find_one({"name" : prof_name})
        prof_url = prof_doc.get("website")
        result_urls.insert(0, prof_url)
    
    return result_urls

def processQuery(search_query):
    
    print("\nResults for:" , search_query, "\n")
    
    results = search_engine(search_query)
    
    total_results = len(results)
    total_pages = math.ceil((len(results))/5)
    page_num = 1
    option = ""
    while option != "q":
        
        start_index = page_num*5 - 5
        end_index = page_num*5
        if end_index > total_results - 1:
            end_index = total_results
        result_page = results[start_index:end_index]
        
        print("\nCPP Faculty Research Interest Search Engine")
        print("Query:", search_query)
        print("Results:", total_results)
        print("Page:", page_num)
        for i,result in enumerate(result_page):
            print((i + start_index + 1), ".", result)
        
        
        print("\n######### Menu ##############")
        if page_num < total_pages:
            print("#n - Next page")
        if page_num > 1:
            print("#p - Previous page")
        print("#q - Quit")
        
        print("")
        option = input("Enter a menu choice: ")
        
        if page_num < total_pages and option == "n":
            page_num += 1
        elif page_num > 1 and option == "p":
            page_num -= 1
        elif option == "q":
            print("Exiting search results")
        else:
            print("Invalid input!\n")
        
    
    

# print menu for search engine
print("\nCPP Faculty Research Interest Search Engine")
print("######### Menu ##############")
print("#a - Search")
print("#q - Quit")

option = ""
while option != "q":
    
    print("")
    option = input("Enter a menu choice: ")

    if option == "a":

        search_query = input("Enter search query: ")
        processQuery(search_query)
        option = "q"
        
    elif option == "q":
        print("Exiting search engine")
    
    else:
        print("Invalid input!")
