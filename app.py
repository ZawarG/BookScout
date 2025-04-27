from flask import Flask, render_template, request
from bookclass import Book


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    user_query = request.args.get('query')
    
    # Passing search query into bookclass
    info = Book(user_query)
    
    # Render the 'book' page and pass query and info
    print(info.title, info.pagecount,info.pubyear,info.categories)
    return render_template('book.html', book_title = info.title, 
                                        book_description = info.description, 
                                        book_image = info.cover,
                                        book_author = info.author,
                                        book_pagecount = info.pagecount,
                                        book_year = info.pubyear,
                                        book_genre = info.categories)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=False)