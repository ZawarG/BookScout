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

    return outputlist
