# search engine interface

def search_engine(search_query):
    # return results ranked
    
    # results
    mock_result = ["https://www.cpp.edu/faculty/prof1/", "https://www.cpp.edu/faculty/prof2/"
                   , "https://www.cpp.edu/faculty/prof3/", "https://www.cpp.edu/faculty/prof4/"
                   , "https://www.cpp.edu/faculty/prof5/", "https://www.cpp.edu/faculty/prof6/"
                   , "https://www.cpp.edu/faculty/prof7/", "https://www.cpp.edu/faculty/prof8/"
                    , "https://www.cpp.edu/faculty/prof9/", "https://www.cpp.edu/faculty/prof10/",
                    "https://www.cpp.edu/faculty/prof11/", "https://www.cpp.edu/faculty/prof12/" ]

    
    return mock_result

def processQuery(search_query):
    
    print("\nResults for:" , search_query, "\n")
    
    results = search_engine(search_query)
    
    total_results = len(results)
    total_pages = len(results)//5 + 1
    page_num = 1
    option = ""
    while option != "q":
        
        start_index = page_num*5 - 5
        end_index = page_num*5
        if end_index >= total_results - 1:
            end_index = total_results
        result_page = results[start_index:end_index]
        
        print("\nCPP Faculty Research Interest Search Engine")
        print("Query:", search_query)
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
