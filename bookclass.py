import json
from urllib.request import urlopen
#from CategoryFinder import category_picker

#APIs 
gapi = "https://www.googleapis.com/books/v1/volumes?q=title:"
oapi = "https://openlibrary.org"


#function to parse api data to find keywords
def category_picker(word_list):
    genres = ['Fiction', 'Fantasy', 'Horror', 'Dystopian', 'True crime', 'Romance', 
              'Comedy', 'Contemporary', 'Thrillers', 'Mystery', 'Psychological', 'Suspense', 
              'Adventure', 'Non Fiction', 'Classicals', 'Science Fiction', 
              'Philosophical', 'Poetry', 'Biography', 'Religious', 'Self Help', 'Mental Health',
              'Productivity', 'Ancient', 'Philosophy', 'Spirituality', 'Parenting', 'Political', 
                'International Relations', 'Business', 'Short Stories', 'Science']

    processedlist = []
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
    
    if 'Fiction' and 'Non Fiction' in outputlist:
        outputlist.remove("Fiction")
    
    if 'Science Fiction' and 'Science' in outputlist:
        outputlist.remove("Science")

    string = ''
    for genre in outputlist:
        string += genre + ' '
    
    return string





class Book:
    def __init__(self, title):
        
        #author, description and pagecount from googlebooks api
        try:
            gbooksapi = urlopen(gapi + title.replace(" ", "%20"))
            book_data = json.load(gbooksapi)
            print("Succesfully Accessed: "+ gapi + title.replace(" ", "%20"))


            for i in range(10):
                volume_info = book_data["items"][i]["volumeInfo"]
                try:
                    self.title = volume_info["title"]
                    print(self.title + '------',title.split(' ')[0])
                    if title.split(' ')[0] in self.title.lower().split(' '):
                        self.author = volume_info["authors"][0]
                        print(self.title)
                        break
                    else:
                        pass
                        print('failed')
                except:
                    self.author = "ERROR"
                    self.title = "Could not find"

            try:    
                self.description = volume_info["description"]
            except:
                for datalists in range(5):
                    try:
                        volume_info = book_data["items"][datalists]["volumeInfo"]
                        self.description = volume_info["description"]
                        break
                    except:
                        self.description = "ERROR"
                        continue
            try:                    
                self.pagecount = volume_info["pageCount"]
            except:
                for datalists in range(5):
                        try:
                            volume_info = book_data["items"][datalists]["volumeInfo"]
                            self.pagecount = volume_info["pageCount"]
                            break
                        except:
                            self.pagecount = "ERROR"
                            continue

        except:
            self.title = title
            self.author = "ERROR"
            self.pagecount = "ERROR"
            self.description = "ERROR"
            print("Failed too access:", gapi + title.replace(" ", "%20"))
    
        try:
            self.cover = json.load(urlopen("https://bookcover.longitood.com/bookcover?book_title="+ self.title.replace(" ","+") + "&author_name=" + self.author.replace(" ","+")))["url"]
            print("Succesfully retrieved bookcover from: ", self.cover)
        except:
            try:
                self.cover = json.load(urlopen("http://localhost:8000/bookcover?book_title="+ self.title.replace(" ","+") + "&author_name=" + self.author.replace(" ","+")))["url"]
                print("Succesfully retrieved bookcover from: ", self.cover, 'using localhost')
            except:
                self.cover = "ERROR"
                print("Failed too find Bookcover from: ", "https://bookcover.longitood.com/bookcover?book_title="+ self.title.replace(" ","+") + "&author_name=" + self.author.replace(" ","+") , "and from: ""http://localhost:8000/bookcover?book_title="+ self.title.replace(" ","+") + "&author_name=" + self.author.replace(" ","+"))


        #publicationdate and categories from
        try:
            obooksapi = urlopen(oapi + '/search.json?q=' + self.title.replace(" ", "+")+"&author=" + self.author.replace(' ','+')) 
            general_info = json.load(obooksapi)
            book_key = general_info['docs'][0]['key']


            obooksapi = urlopen(oapi + f'{book_key}.json')  
            specific_info = json.load(obooksapi)
            categorylist = specific_info['subjects']


            print("Succesfully Accessed: ", oapi + '/search.json?q=' + self.title.replace(" ", "+")+"&author=" + self.author.replace(' ','+'))
            try:
                self.categories = category_picker(categorylist)
            except:
                self.categories = ["ERROR"]
            try:
                pubyears = []
                for datalist in range(5):
                    try:
                        general_info = general_info['docs'][datalist]
                        pubyears.append(general_info["first_publish_year"])
                    except:
                        pass
                self.pubyear = min(pubyears)
            except:
                self.pubyear = "ERROR"
        
        except:
            self.categories = "ERROR"
            self.pubyear = "ERROR"
            print("Failed too access:", oapi + '/search.json?q=' + self.title.replace(" ", "+")+"&author=" + self.author.replace(' ','+'))
