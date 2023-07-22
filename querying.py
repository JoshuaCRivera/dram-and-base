import sqlite3, math
from db_handling import *
'''
File for all querying operations the user has access to. Functions as a sort of API.
'''


'''
Queries the database using SQL syntax.
Output: tuple of number_of_results, results
'''
def query(query: str):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()
    rows = cursor.execute(query).fetchall()
    connection.close()
    return len(rows), rows

'''
Calculates the similarity between two dramas as normalized vectors.
The similarity is 1 - normalized euclidean distance
'''
def similarity(drama1: str, drama2: str):
    try:
        drama_vec1 = drama_vector(drama1)
    except:
        drama_vec1 = average_of_all(drama1)
    try:
        drama_vec2 = drama_vector(drama2)
    except:
        drama_vec2 = average_of_all(drama2)

    dist = math.dist(drama_vec1, drama_vec2)
    # normalize so that 0 < sim < 1
    sim = (1 - (dist / math.sqrt(len(numeric_cols))))**2
    sim = round(sim, 3)
    return sim

'''
Takes in drama by title (if unique) and calculates similarities to all other dramas.
Takes top k (choosable, default 5) and outputs their titles + IDs and similrity scores as list of tuples
'''
def top_k_most_similar(drama: str, k=5):
    all_dramas_query = "SELECT title, id FROM dramas"
    _, all_dramas = query(all_dramas_query)
    all_dramas = [tuple(d) for d in all_dramas]
    all_listed = []
    for other_title, other_drama in all_dramas:      # other_drama is id
        all_listed.append((similarity(drama, other_drama), other_drama, other_title))
    all_listed.sort(key=lambda x:x[0], reverse=True)
    return all_listed [1:k+1]   # top drama will always be drama itself, so we cut it off

def most_similar_graph(drama: str):
    # put nx graph code here
    pass