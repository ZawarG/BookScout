from flask import Flask, render_template, request
from BackendBookInfo.bookclass import Book


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
    return render_template('book.html', book_title = info.title, book_description = info.description)

if __name__ == '__main__':
    app.run(debug=True)