import os
import csv
import json

# Load paths
parentDir = os.path.dirname(os.path.abspath(__file__))
    
users_file = os.path.join(parentDir, '..', 'data', 'Users.csv')
users_file = os.path.abspath(users_file)

books_file = os.path.join(parentDir, '..', 'data', 'Books.csv')
books_file = os.path.abspath(books_file)

ratings_file = os.path.join(parentDir, '..', 'data', 'Ratings.csv')
ratings_file = os.path.abspath(ratings_file)

ratings = []
books = []




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Save implicit ratings graph ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('⏳ Starting save implicit ratings graph...')
user_book_list = {}
book_user_list = {}

with open(ratings_file, newline='', encoding='utf-8') as open_ratings_file:
    csv_reader = csv.DictReader(open_ratings_file)
    
    print('⏳ Scanning ratings...')
    for rating in csv_reader:
        user = rating['userID']
        book = rating['isbn']

        ratings.append(rating)

        try:
            user_book_list[user].append(book)
        except:
            user_book_list[user] = [book]

        try:
            book_user_list[book].append(user)
        except:
            book_user_list[book] = [user]
    print('✅ Success')

# Save the dictionary to a JSON file
print('⏳ Saving ratings...')
dest_file = os.path.join(parentDir, '..', 'data', 'user_book_list.json')
dest_file = os.path.abspath(dest_file)
with open(dest_file, 'w') as json_file:
    json.dump(user_book_list, json_file, indent=2)

dest_file = os.path.join(parentDir, '..', 'data', 'book_user_list.json')
dest_file = os.path.abspath(dest_file)
with open(dest_file, 'w') as json_file:
    json.dump(book_user_list, json_file, indent=2)
print('✅ Success')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Save indexed books ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('⏳ Starting save book indexed json...')
indexed_books = {}

print('⏳ Scanning books...')
with open(books_file, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)

    for book in csv_reader:
        books.append(book)
        indexed_books[book['isbn']] = { 'isbn': book['isbn'],
                                        'bookTitle': book['bookTitle'],
                                        'bookAuthor': book['bookAuthor'],
                                        'yearOfPublication': book['yearOfPublication'],
                                        'publisher': book['publisher'],
                                        'imageURL_s': book['imageURL_s'],
                                        'imageURL_m': book['imageURL_m'],
                                        'imageURL_l': book['imageURL_l'],
                                        'avgRating': book['avgRating'],
                                        'countRating': book['countRating'] }
        
print('⏳ Saving books...')
dest_file = os.path.join(parentDir, '..', 'data', 'indexed_books.json')
dest_file = os.path.abspath(dest_file)
with open(dest_file, 'w') as json_file:
    json.dump(indexed_books, json_file, indent=2)
print('✅ Success')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Save users avg rating ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('⏳ Starting save users avg ratings...')
users_ratings = {}
users_avg_rating = {}

print('⏳ Scanning ratings...')
for rating in ratings:
    user  = rating['userID']
    bookRating = rating['bookRating']

    if bookRating != "0":
        try:
            users_ratings[user].append(int(bookRating))
        except:
            users_ratings[user] = [int(bookRating)]

for userID, bookRatings in users_ratings.items():
    if len(bookRatings) == 0:
        avg = 0.0
    else:
        total_sum = sum(bookRatings)
        avg = total_sum / len(bookRatings)
    
    avg = "{:.2f}".format(avg)

    users_avg_rating[userID] = avg
print('✅ Success')


print('⏳ Saving avg...')
dest_file = os.path.join(parentDir, '..', 'data', 'users_avg_rating.json')
dest_file = os.path.abspath(dest_file)

with open(users_file, newline='', encoding='utf-8') as open_users_file:
    csv_reader = csv.DictReader(open_users_file)

    for u in csv_reader:
        userID = u['userID']
        try:
            temp = users_avg_rating[userID]
        except:
            users_avg_rating[userID] = "0.0"

with open(dest_file, 'w') as json_file:
    json.dump(users_avg_rating, json_file, indent=2)
print('✅ Success')
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



print("✅ Set Up successful")