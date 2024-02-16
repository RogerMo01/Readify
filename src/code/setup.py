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



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~ Save implicit ratings graph ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
user_book_list = {}
book_user_list = {}

# Scan all books
with open(ratings_file, newline='', encoding='utf-8') as open_ratings_file:
    csv_reader = csv.DictReader(open_ratings_file)
    
    print('⏳ Scanning ratings...')
    for rating in csv_reader:
        user = rating['userID']
        book = rating['isbn']

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


