# 📚 Book Search Web App

A clean and responsive web application that allows users to search for books by title. Built using Flask, HTML, CSS, and JavaScript, the app fetches data from the OpenLibrary and Google Books APIs and displays detailed information about the searched book.

## Features

-  Search for books by title
-  Displays:
    - Book title
    - Author(s)
    - Description
    - Page count
    - Genres
    - Publication year
-  Uses:
    - [OpenLibrary API](https://openlibrary.org/developers/api)
    - [Google Books API](https://developers.google.com/books)
    - [W3slley's Bookcover API](https://github.com/w3slley/bookcover-api).

##  Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **APIs:** Google Books API, OpenLibrary API, W3slley's Bookcover API
  
## How It Works

The frontend, built using Flask and standard web technologies, takes a user's search input and sends it to `bookclass.py`, which handles the logic for fetching and compiling book data. Here's a step-by-step breakdown:

1. **Google Books API Search**  
   The app queries the Google Books API to find a match for the searched title.

2. **Primary Data Extraction from GoogleBooks API**  
   - If a match is found, the book's title, author(s), description, and page count are extracted.  
   - If no match is found, the user is shown an error page displaying the top 5 closest matches from the Google Books API.

3. **Cover Image Retrieval**  
   W3slley's API is used to fetch a book cover image.

4. **Secondary Data Extraction from OpenBooks API**  
   The book is also queried on the OpenLibrary API to:
   - Locate a specific key associated with the book.  
   - Parse the `subjects` section to determine relevant genres.  
   - Identify the earliest available publication date.

5. **Display**  
   All gathered information is rendered and displayed to the user in a clean, responsive web interface.
