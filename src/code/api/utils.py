import math
import os

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SEARCH ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def graph_search(user_books, book_user_list, user_book_list, show_log=True):
    readers = {}
    readers_count = {}
    l1 = list(map(lambda x : x[0], user_books.items()))
    l2 = set([])
    l3 = set([])

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
                    readers_count[b2] = 1
    
    if show_log:
        log('\n[*] Graph search results:')
        log(f'User spread to {len(l1)} books')
        log(f'l1 spread to {len(l2)} neighbors')
        log(f'l2 spread to {len(l3)} recommended books')
    
    return l1, l2, l3, readers, readers_count
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RANKING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def count_sorter(l3, readers_count):
    return list(sorted(l3, key=lambda x: readers_count.get(x, 0), reverse=True))

def pearson_prediction_sorter(books, sim, closest_neigthbors, matrix, avg, user_avg):
    books_predictions = {}
    for p in books:
        acc_up = 0
        acc_down = 0

        for v in closest_neigthbors:
            if p in matrix[v]:
                acc_up += (sim[v] * (float(matrix[v][p]) - float(avg[v])))
            else:
                acc_up += 0
            acc_down += sim[v]
                
        pred = user_avg + (acc_up/acc_down)

        books_predictions[p] = pred

    return list(sorted(books, key=lambda x: books_predictions.get(x, 0), reverse=True)), books_predictions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SELECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pearson_neighborhood(User, l2, l3, explicit_matrix, avg, user_books, readers, user_avg, show_log=True):
    
    pearson_coefficients = {} # {'userId': coeficient}

    for user in l2:
        if user in explicit_matrix:
            pearson_coefficients[user] = sim_Pearson(User, user, explicit_matrix, avg, user_avg)

    closest_neigthbors = [key for key, value in list(pearson_coefficients.items()) if value > 0]

    available_books = []
    for b in l3:
        for r in readers[b]:
            if r in closest_neigthbors:
                available_books.append(b)
                break

    if show_log:
        log('\n[*] Pearson coefficient results:')
        log(f'Neigthbors with Pearson coefficient grater than 0: {len(closest_neigthbors)}')
        log(f'Book reduction by nearby neighbors from {len(l3)} books to {len(available_books)}')
    
    return available_books, pearson_coefficients, closest_neigthbors

def sim_Pearson(User, b, matrix, avg, user_avg):
    r_ap_list = []
    r_bp_list = []

    # Save common ratings
    for book in list(matrix[User].keys()):
        if book in list(matrix[b].keys()):
            r_ap_list.append(float(matrix[User][book]))
            r_bp_list.append(float(matrix[b][book]))
    
    size = len(r_ap_list)

    if size == 0:
        return -1

    up = sum([(r_ap_list[i] - user_avg) * (r_bp_list[i] - float(avg[b])) for i in range(size)])

    acc_l = 0
    acc_r = 0
    for i in range(size):
        acc_l += (r_ap_list[i] - user_avg)**2
        acc_r += (r_bp_list[i] - float(avg[b]))**2

    down = math.sqrt(acc_l) + math.sqrt(acc_r)
    return up/(down + 0.000000000001)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'log.txt')
log_path = os.path.abspath(log_path)

def log(log):
    with open(log_path, 'a') as file:
        file.write(log + '\n')
