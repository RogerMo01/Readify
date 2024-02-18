import math

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ RANKING ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def count_sorter(l3, readers_count):
    return list(sorted(l3, key=lambda x: readers_count.get(x, 0), reverse=True))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SELECTION ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def pearson_neighborhood(l1, l2, l3, explicit_matrix, avg, user_books, readers):
    User = "X"

    # Add user to matrix
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

    pearson_coefficients = {} # {'userId': coeficient}

    for user in l2:
        if user in explicit_matrix:
            pearson_coefficients[user] = sim_Pearson(User, user, explicit_matrix, avg, user_avg)

    closest_neigthbors = [key for key, value in list(pearson_coefficients.items()) if value > 0]

    print(f'Neigthbors with Pearson coefficient grater than 0: {len(closest_neigthbors)}')

    available_books = []
    for b in l3:
        for r in readers[b]:
            if r in closest_neigthbors:
                available_books.append(b)
                break

    print(f'Book reduction by nearby neighbors from {len(l3)} books to {len(available_books)}')
    
    return available_books

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
    return up/(down)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
