import json
import os
import csv
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.utils import graph_search, pearson_neighborhood, count_sorter, pearson_prediction_sorter, log
from api.trie import Trie
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

stop_words_english = set(stopwords.words('english'))
stop_words_spanish = set(stopwords.words('spanish'))



# Runtime loaded data
User = "X"
all_books_data = []
indexed_books = {}
user_books = {}
user_book_list = {}
book_user_list = {}
readers = {}
readers_count = {}
explicit_matrix = {}
users_avg_rating = {}


# Data paths
csv_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'data', 'Books.csv')
csv_file_path = os.path.abspath(csv_file_path)

user_books_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'data', 'user_books.json')
user_books_path = os.path.abspath(user_books_path)

user_book_list_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'data', 'user_book_list.json')
user_book_list_path = os.path.abspath(user_book_list_path)

book_user_list_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'data', 'book_user_list.json')
book_user_list_path = os.path.abspath(book_user_list_path)

indexed_books_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'data', 'indexed_books.json')
indexed_books_path = os.path.abspath(indexed_books_path)

explicit_matrix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'explicit_ratings_matrix.json')
explicit_matrix_path = os.path.abspath(explicit_matrix_path)

books_by_word_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '..', '..', 'data', 'books_by_word.json')
books_by_word_path = os.path.abspath(books_by_word_path)

users_avg_rating_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'users_avg_rating.json')
users_avg_rating_path = os.path.abspath(users_avg_rating_path)

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'config.json')
config_path = os.path.abspath(config_path)

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'log.txt')
log_path = os.path.abspath(log_path)


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Load runtime variables ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
with open(books_by_word_path, 'r') as books_by_word_file:
    books_by_word = json.load(books_by_word_file)
trie = Trie(books_by_word)
print("✅ Load end")
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





def add_user_to_matrix(l1):
    user_ratings = []
    for b in l1:
        rat = user_books[b]['rating']
        if User in explicit_matrix:
            explicit_matrix[User][b] = rat
        else:
            explicit_matrix[User] = {b: rat}
        user_ratings.append(float(rat))
    return user_ratings

def load_configuration():
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    selection_method = config['selection']
    ranking_method = config['ranking']
    limit = int(config['limit'])
    return selection_method, ranking_method, limit




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Recommendation APIs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@api_view(['GET'])
def main_recommendation(request):
    log('\n\n\n[----------------- GET -----------------]')
    # Main books recommender function
    l1, l2, l3, readers, readers_count = graph_search(user_books, book_user_list, user_book_list)

    # Load configuration
    selection_method, ranking_method, limit = load_configuration()

    # Add user to matrix
    user_ratings = add_user_to_matrix(l1)

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
    c = 0
    for b in ranked_set:
        if c == limit:
            break
        elif b not in user_books and b in indexed_books:
            limited_ranked_set.append(b)
            c += 1

            
    # Show log
    log('\n[*] Rank results:')
    if ranking_method == "pearson_based_prediction":
        for x in limited_ranked_set:
            log(f'isbn: {x} ({round(predictions[x], 2)} rank prediction)')
    else:
        for x in limited_ranked_set:
            log(f'isbn: {x} ({readers_count[x]} times)')
    
    
    # Delete User from matrix
    if User in explicit_matrix:
        del explicit_matrix[User]

    # Map data
    request_response = list(map(lambda x: indexed_books[x], limited_ranked_set))

    return Response({'data': request_response})


@api_view(['GET'])
def author_recommendation(request):
    response = {
        'author': "",
        'list': []
    }

    if len(list(user_books.items())) == 0:
        Response(response)

    listed_user_books = list(user_books.items())
    
    user_ratings_by_author = {}
    for _, i in listed_user_books:
        if i['author'] in user_ratings_by_author:
            user_ratings_by_author[i['author']].append(float(i["rating"]))
        else:
             user_ratings_by_author[i['author']] = [float(i["rating"])]

    maxAuthor = ""
    maxAvg = 0
    for a, l in list(user_ratings_by_author.items()):
        avg = sum(l)/len(l)
        if avg > maxAvg:
            maxAvg = avg
            maxAuthor = a

    l1, l2, l3, readers, readers_count = graph_search(user_books, book_user_list, user_book_list, False)

    # Load configuration
    selection_method, ranking_method, limit = load_configuration()
    
    # Add user to matrix
    user_ratings = add_user_to_matrix(l1)

    # Calculate user avg
    user_avg = 0
    if len(user_ratings) > 0:
        user_avg = sum(user_ratings)/len(user_ratings)


    # 📊 Switch on set selection method
    if selection_method == "pearson":
        selected_set, pearson_coefficients, closest_neigthbors = pearson_neighborhood(User, l2, l3, explicit_matrix, users_avg_rating, user_books, readers, user_avg, False)
    else:
        selected_set = l3


    # 📉 Switch on ranking method
    if ranking_method == "pearson_based_prediction":
        ranked_set, predictions = pearson_prediction_sorter(selected_set, pearson_coefficients, closest_neigthbors, explicit_matrix, users_avg_rating, user_avg)
    else:
        ranked_set = count_sorter(selected_set, readers_count)
    

    # 🔚 Switch on rank limit
    limited_ranked_set = []
    c = 0
    for b in ranked_set:
        if c == limit:
            break
        elif b not in user_books and b in indexed_books and indexed_books[b]['bookAuthor'] == maxAuthor:
            limited_ranked_set.append(b)
            c+=1
    
    # Delete User from matrix
    if User in explicit_matrix:
        del explicit_matrix[User]

    # Map data
    request_list = list(map(lambda x: indexed_books[x], limited_ranked_set))

    response = {
        'author': maxAuthor,
        'list': request_list
    }

    return Response(response)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Other APIs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@api_view(['GET'])
def filter_books(request):
    # Search for user query

    query = request.GET.get('query', '')
    if not query:
        return Response({'data': final_answer})
    split_query = query.lower().split()

    final_answer = []
    books = []

    for item in split_query:
        if item not in stop_words_english and item not in stop_words_spanish and item.isalpha():
            (word_end, isbn_books) = trie.search(item)
            if word_end:
                books.append(isbn_books)

    if books:
        union_books = set.union(*map(set, books))
    else:
        union_books = set()

    response = {}
    if len(union_books) != 0:
        for isbn in union_books:
            book = indexed_books[isbn]
            word_counter = 0
            split_title = book['bookTitle'].lower().split()
            for item in split_query:
                if item in split_title:
                    word_counter += 1
            response[isbn] = word_counter

    descending_sorted_dictionary = {k: v for k, v in sorted(
        response.items(), key=lambda item: item[1], reverse=True)}

    ub = list(user_books.keys())

    count = 0
    for isbn in descending_sorted_dictionary.keys():
        if count == 50:
            break
        if isbn not in ub:
            final_answer.append(indexed_books[isbn])
            count += 1

    return Response({'data': final_answer})


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

        user_books[isbn] = {'rating': rating,
                            'title': title, 'author': author, 'cover': cover}

        # Save json
        with open(user_books_path, 'w') as user_books_file:
            json.dump(user_books, user_books_file, indent=2)

        return Response({'message': "OK"})
    except Exception as e:
        return Response({'message': str(e)}, status=400)
    
@api_view(['GET'])
def get_config(request):
    # Load configuration
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return Response(config)

@api_view(['POST'])
def set_config(request):
    try:
        new_config = json.loads(request.body.decode('utf-8'))

        # Save json
        with open(config_path, 'w') as config_file:
            json.dump(new_config, config_file, indent=2)

        return Response({'message': "OK"})
    except Exception as e:
        return Response({'message': str(e)}, status=400)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

