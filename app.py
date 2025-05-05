from flask import Flask, render_template, request
from bookclass import book_import


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    user_query = request.args.get('query')
    
    # Passing search query into bookclass
    info = book_import(user_query)
    
    if info.title != "ERROR":
        print(info.title)
        # Render the 'book' page and pass query and info
        return render_template('book.html', book_title = info.title, 
                                            book_description = info.description, 
                                            book_image = info.cover,
                                            book_author = info.author,
                                            book_pagecount = info.pagecount,
                                            book_year = info.pubyear,
                                            book_genre = info.categories)
    else:
        return render_template ('error.html', user_query = user_query, book_list = info.suggestions)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=False)