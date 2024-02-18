import json
import os
import csv
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils import pearson_neighborhood, count_sorter, pearson_prediction_sorter

# Runtime loaded data
all_books_data = []
indexed_books = {}
user_books = {}
user_book_list = {}
book_user_list = {}
l3 = set([])
readers = {}
readers_count = {}
explicit_matrix = {}
users_avg_rating = {}


# Data paths
csv_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'Books.csv')
csv_file_path = os.path.abspath(csv_file_path)

user_books_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'user_books.json')
user_books_path = os.path.abspath(user_books_path)

user_book_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'user_book_list.json')
user_book_list_path = os.path.abspath(user_book_list_path)

book_user_list_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'book_user_list.json')
book_user_list_path = os.path.abspath(book_user_list_path)

indexed_books_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'indexed_books.json')
indexed_books_path = os.path.abspath(indexed_books_path)

explicit_matrix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'explicit_ratings_matrix.json')
explicit_matrix_path = os.path.abspath(explicit_matrix_path)

users_avg_rating_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'users_avg_rating.json')
users_avg_rating_path = os.path.abspath(users_avg_rating_path)

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'config.json')
config_path = os.path.abspath(config_path)


# Start load
print("⏳ Load started")
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    all_books_data = list(csv_reader)

try:
    with open(user_books_path, 'r') as user_books_file:
        user_books = json.load(user_books_file)
except:
    user_books = {}
    with open(user_books_path, 'w') as user_books_file:
        json.dump(user_books, user_books_file, indent=2)

with open(user_book_list_path, 'r') as user_book_list_file:
    user_book_list = json.load(user_book_list_file)
with open(book_user_list_path, 'r') as book_user_list_file:
    book_user_list = json.load(book_user_list_file)
with open(indexed_books_path, 'r') as indexed_books_file:
    indexed_books = json.load(indexed_books_file)
with open(explicit_matrix_path, 'r') as explicit_matrix_file:
    explicit_matrix = json.load(explicit_matrix_file)
with open(users_avg_rating_path, 'r') as users_avg_rating_file:
    users_avg_rating = json.load(users_avg_rating_file)
print("✅ Load end")



@api_view(['GET'])
def main_recommendation(request):
    # Main books recommender function
    
    readers = {}
    readers_count = {}
    l1 = list(map(lambda x : x[0], user_books.items()))
    l2 = set([])

    # Graph Search
    for b in l1:
        for u in book_user_list[b]:
            l2.add(u)
            for b2 in user_book_list[u]:
                try:
                    readers[b2].append(u)
                    readers_count[b2]+=1
                except:
                    l3.add(b2)
                    readers[b2] = [u]
                    readers_count[b2] = 0

    print(f'User spread to {len(l1)} books')
    print(f'l1 spread to {len(l2)} neighbors')
    print(f'l2 spread to {len(l3)} recommended books')

    # Load configuration
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    selection_method = config['selection']
    ranking_method = config['ranking']
    limit = int(config['limit'])

    # Add user to matrix
    User = "X"
    user_ratings = []
    for b in l1:
        rat = user_books[b]['rating']
        if User in explicit_matrix:
            explicit_matrix[User][b] = rat
        else:
            explicit_matrix[User] = {b: rat}
        user_ratings.append(float(rat))

    # Calculate user avg
    user_avg = 0
    if len(user_ratings) > 0:
        user_avg = sum(user_ratings)/len(user_ratings)


    pearson_coefficients = {} #{'userId': coeficient}
    closest_neigthbors = []
    

    # 📊 Switch on set selection method
    if selection_method == "pearson":
        selected_set, pearson_coefficients, closest_neigthbors = pearson_neighborhood(User, l2, l3, explicit_matrix, users_avg_rating, user_books, readers, user_avg)
    else:
        selected_set = l3

    

    # 📉 Switch on ranking method
    if ranking_method == "pearson_based_prediction":
        ranked_set, predictions = pearson_prediction_sorter(selected_set, pearson_coefficients, closest_neigthbors, explicit_matrix, users_avg_rating, user_avg)
    else:
        ranked_set = count_sorter(selected_set, readers_count)
    


    # 🔚 Switch on rank limit
    limited_ranked_set = []
    if len(ranked_set) > limit:
        c = 0
        for b in ranked_set:
            if c == limit:
                break
            elif b not in user_books:
                limited_ranked_set.append(b)
                c+=1
    else:
        limited_ranked_set = ranked_set



    # Show log
    print('\n~~~~~~~~~~~~~ Rank: ~~~~~~~~~~~~~')
    if ranking_method == "pearson_based_prediction":
        for x in limited_ranked_set:
            print(f'{x} ({round(predictions[x], 2)} rank prediction)')
    else:
        for x in limited_ranked_set:
            print(f'{x} ({readers_count[x]} times)')
    
    
    # Delete User from matrix
    del explicit_matrix[User]

    # Map data
    request_response = list(map(lambda x: indexed_books[x], limited_ranked_set))

    return Response({'data': request_response})


@api_view(['GET'])
def filter_books(request):
    # Search for user query

    ub = list(user_books.items())

    count = 0
    response = []

    for book in all_books_data:
        if count == 10:
            break
        
        if any(x[0] == book['isbn'] for x in ub):
            continue
        else:
            response.append(book)
            count+=1

    return Response({'data': response})

@api_view(['GET'])
def user_books_list(request):
    # List of user rated books
    return Response({'data': list(user_books.items())})

@api_view(['POST'])
def add_book_to_user(request):
    try:
        data = json.loads(request.body.decode('utf-8'))

        isbn = data.get('isbn')
        title = data.get('bookTitle')
        author = data.get('bookAuthor')
        cover = data.get('imageURL_s')
        rating = data.get('rating')

        user_books[isbn] = {'rating': rating, 'title': title, 'author': author, 'cover': cover}

        # Save json
        with open(user_books_path, 'w') as user_books_file:
            json.dump(user_books, user_books_file, indent=2)

        return Response({'message': "OK"})
    except Exception as e:
        return Response({'message': str(e)}, status=400)