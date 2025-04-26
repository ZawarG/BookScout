import json
from urllib.request import urlopen
from CategoryFinder import category_picker

gapi = "https://www.googleapis.com/books/v1/volumes?q=title:"
oapi = "https://openlibrary.org/search.json?q="

class Book:
    def __init__(self, title):
        
        #author, description and pagecount from googlebooks api
        try:
            gbooksapi = urlopen(gapi + title.replace(" ", "%20"))
            book_data = json.load(gbooksapi)
            volume_info = book_data["items"][0]["volumeInfo"]
            print("Succesfully Accessed: "+ gapi + title.replace(" ", "%20"))
            try:
                self.title = volume_info["title"]
                self.author = volume_info["authors"][0]   
            except:
                self.author = "ERROR"

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
            obooksapi = urlopen(oapi + self.title.replace(" ", "+")+"&author=" + self.author.replace(' ','+'))  
            book_data = json.load(obooksapi) 
            volume_info = book_data['docs'][0]
            categorylist = volume_info['subject']
            print("Succesfully Accessed: ", oapi + self.title.replace(" ", "+")+"&author=" + self.author.replace(' ','+'))
            try:
                self.categories = category_picker(categorylist)
            except:
                self.categories = ["ERROR"]
            try:
                pubyears = []
                for datalist in range(5):
                    volume_info = book_data['docs'][datalist]
                    pubyears.append(volume_info["first_publish_year"])
                self.pubyear = min(pubyears)
            except:
                self.pubyear = "ERROR"
        
        except:
            self.categories = "ERROR"
            self.pubyear = "ERROR"
            print("Failed too access:", oapi + self.title.replace(" ", "+")+"&author=" + self.author.replace(' ','+'))


#check functioning
#a = Book('harry potter and the philosophers stone')
#print(a.description)