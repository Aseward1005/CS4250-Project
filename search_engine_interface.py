# search engine interface


def processQuery(searchQuery):
    
    print("Processing search query")
    
    

# print menu for search engine
print("CPP Faculty Research Interest Search Engine")
print("######### Menu ##############")
print("#a - Search")
print("#q - Quit")

option = ""
while option != "q":
    
    print("")
    option = input("Enter a menu choice: ")

    if option == "a":

        searchQuery = input("Enter search query: ")
        processQuery(searchQuery)
        
    elif option == "q":
        print("Exiting search engine")
    
    else:
        print("Invalid input!")
