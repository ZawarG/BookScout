import json
from urllib.request import urlopen


#API links
gapi = "https://www.googleapis.com/books/v1/volumes?q=title:"
oapi = "https://openlibrary.org"



#parse api data to return a list of categories from keywords
def category_picker(word_list):
    genres = ['Fiction', 'Fantasy', 'Horror', 'Dystopian', 'True crime', 'Romance', 
              'Comedy', 'Contemporary', 'Thrillers', 'Mystery', 'Psychological', 'Suspense', 
              'Adventure', 'Non Fiction', 'Classicals', 'Science Fiction', 
              'Philosophical', 'Poetry', 'Biography', 'Religious', 'Self Help', 'Mental Health',
              'Productivity', 'Ancient', 'Philosophy', 'Spirituality', 'Parenting', 'Political', 
                'International Relations', 'Business', 'Short Stories', 'Science']


    processedlist = []
    #searching for keywords in list from api (sometimes looks like 'fiction books east asia', so this searches for the word fiction)
    for genre in genres:
        for phrase in word_list:
            if genre.replace('-',' ').lower() == phrase.replace('-', ' ').lower():
                processedlist.append(genre)
            else:
                words = phrase.split()
                for word in words:
                    if genre.lower() == word.lower():
                        processedlist.append(genre)
                        break
        
    outputlist = []
    for genre in processedlist:
        if genre not in outputlist:
            outputlist.append(genre)

    #removing repetitive phrases
    if 'Fiction' and 'Non Fiction' in outputlist:
        outputlist.remove("Fiction")
    
    if 'Science Fiction' and 'Science' in outputlist:
        outputlist.remove("Science")

    #returning a string for website output
    string = ''
    for genre in outputlist:
        string += genre + ', '
    string = string.rstrip(', ')

    return string


class Book:
    def __init__(self, title):
        self.title = title
        self.author = ''
        self.pubyear = ''
        self.pagecount = ''
        self.cover = ''
        self.categories = ''
        self.suggestions = []
        self.description = ''

        #googlebooks data
        self.gbooks_data = []
        self.gbooks_info = []

        #openbooks data
        self.obooks_info = []
        self.obooks_data = []

        
    
    #accessing google link to first check if the book exists, get a list of alternative titles if it doesnt
    def initial_title_check(self):
        try:
            gbooksapi = urlopen(gapi + self.title.replace(" ", "%20"))
            gbook_data = json.load(gbooksapi)
            #check first 10 titles
            for i in range(5):
                gbooks_info = gbook_data["items"][i]["volumeInfo"]

                try:
                    title = gbooks_info["title"]
                    self.suggestions.append(gbooks_info["title"])
                    
                    
                    if title.split(' ')[0].lower() in self.title.lower().split(' '):
                        self.title = title
                        self.author = gbooks_info["authors"][0]
                        self.gbooks_data = gbook_data
                        self.gbooks_info = gbooks_info
                        break
                    else:
                        self.title = 'ERROR'
                except:
                    pass
        except:
            self.title = 'ERROR'


    #getting description from googlebooks data
    def get_description(self):
        try:
            self.description = self.gbooks_info["description"]
        #if not found than use description from other titles, usually when you search for a book all the results are the same book with different publishers
        except:
            try:
                for books in range(5):
                    try:
                        volume_info = self.gbooks_data["items"][books]["volumeInfo"]
                        self.description = volume_info["description"]
                        break
                    except:
                        self.description = "ERROR"
                        continue
            except:
                self.description = 'ERROR'
    
    #getting pagecount also from googlebooks data
    def get_pagecount(self):
        try:
            self.pagecount = self.gbooks_info["pageCount"]
        #if not found than use pagecount from other titles, usually when you search for a book all the results are the same book with different publishers
        except:
            try:
                for books in range(5):
                    try:
                        volume_info = self.gbooks_data["items"][books]["volumeInfo"]
                        self.pagecount = volume_info["pageCount"]
                        break
                    except:
                        self.pagecount = "ERROR"
                        continue
            except:
                self.pagecount = 'ERROR'
    
    #cover image link found from w3slleys github
    def get_cover(self):
        try:
            self.cover = json.load(urlopen("https://bookcover.longitood.com/bookcover?book_title="+ self.title.replace(" ","+") + "&author_name=" + self.author.replace(" ","+")))["url"]
        except:
            self.cover = 'ERROR'
    
    #accessing openbooks data
    def get_openbooksdata(self):
            try:
                obooksapi = urlopen(oapi + '/search.json?q=' + self.title.replace(" ", "+")+"&author=" + self.author.replace(' ','+')) 
                self.obooks_info = json.load(obooksapi)
                book_key = self.obooks_info['docs'][0]['key']

                #openbooks changed their api to be faster by incorporating 
                obooksapi = urlopen(oapi + f'{book_key}.json')  
                self.obooks_data = json.load(obooksapi)
            except:
                #if you dont find the book on openbooks its probably obscure or the websites not being accessible
                self.title = "ERROR"
    
    #categories from the subjects
    def get_categories(self):
        self.categories = category_picker(self.obooks_data['subjects']) 

    #publication year is the smallest number from the first five results of obooks, since they are usually different 
    def get_pubyear(self):
            try:    
                pubyears = []
                for year in range(5):
                    try:
                        info = self.obooks_info['docs'][year]
                        pubyears.append(info["first_publish_year"])
                    except:
                        pass
                self.pubyear = min(pubyears)
            except:
                pass

#function to call in app.py, first checks if the book exists using googlebooks api before moving forward then checking again using openbooks api.
def book_import(title):
    book = Book(title)
    book.initial_title_check()
    if book.title != 'ERROR':
        book.get_description()
        book.get_pagecount()
        book.get_cover()
        book.get_openbooksdata()
        if book.title != 'ERROR':
            book.get_pubyear()
            book.get_categories()
    
    return book
"""
a = book_import("nineteen eighty four")
print(a.pubyear, a.categories)
"""