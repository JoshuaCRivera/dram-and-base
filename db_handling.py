import sqlite3
import math
import numpy as np

columns = []
column_types = {}

def create_drama_db(dramas_dict: dict):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()

    # getting column names and types, translating those to sql (ugly)
    global columns
    global column_types
    columns = list((list(dramas_dict.values())[0].keys()))
    type_dict = {"<class 'int'>": "integer", "<class 'str'>": "text", "<class 'float'>": "real"}
    column_types = {col: type_dict[str(type(list(dramas_dict.values())[0][col]))] for col in columns}
    print(column_types)

    #creating table
    columns_str = ", ".join(f"{col} {column_types[col]}" for col in columns[1:])
    create_query_d = "CREATE TABLE dramas(id text PRIMARY KEY, " + columns_str + ")"
    #print(create_query_d)
    try: 
        cursor.execute(create_query_d)
    except:
        print("table already exists")

    # adding drama data to table
    for drama in dramas_dict.values():
        entries = []
        for col in columns:
            if column_types[col] == 'text':
                entries.append(f"'{drama[col]}'")
            else:
                entries.append(f"{drama[col]}")
        insert_query_d = f"INSERT INTO dramas VALUES(" + ", ".join(entries) + ")"
        #print(insert_query_d)
        try: 
            cursor.execute(insert_query_d)
        except:
            print("drama already in db")
        connection.commit()

    # calculating averages

    mins = []
    maxs = []
    for col in columns:
        full_column = cursor.execute(f"SELECT {col} from DRAMAS WHERE 1=1").fetchall()
        # are these tuples or not? If yes:
        full_column = [row[0] for row in full_column]
        if column_types[col] != 'text':
            mins.append(min(full_column))
            maxs.append(max(full_column))
        else: 
            mins.append('min')
            maxs.append('max')
    cursor.execute("DELETE FROM dramas where id = 'min' OR id = 'max'")
    cursor.execute("INSERT INTO dramas VALUES" + str(tuple(mins)))
    cursor.execute("INSERT INTO dramas VALUES" + str(tuple(maxs)))
    connection.commit()
    connection.close()


def create_characters_db(char_dict):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()
    columns = list(list(char_dict.values())[0].keys())
    type_dict = {"<class 'int'>": "integer", "<class 'str'>": "text", "<class 'float'>": "real"}
    column_types = {col: type_dict[str(type(list(char_dict.values())[0][col]))] for col in columns}
    print(column_types)

    # create table
    columns_str = " ".join(f"{col} {column_types[col]}" for col in columns)
    create_query_c = "CREATE TABLE characters(id text PRIMARY KEY " + columns_str + ")"
    cursor.execute(create_query_c)

    # adding character data to table
    for id, character in char_dict.items():
        # this is a bad way to ensure text comes in ''
        insert_query_c = f"INSERT INTO characters VALUES('{id}'" #TODO change if id integer: remove ''
        for col in columns:
            if column_types[col] == 'text':
                insert_query_c += f", '{character[col]}'"
            else:
                insert_query_c += f", {character[col]}"
        insert_query_d += ")"
        print(insert_query_c)
        cursor.execute(insert_query_c)
        connection.commit()
    connection.close()
        
'''
Calculates the similarity between two dramas. Currently takes IDs --> drama names?
'''
def similarity(drama1: str, drama2: str):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()
    query = "SELECT * from dramas WHERE id = '{}' OR id = '{}'".format(drama1, drama2)
    cursor.execute(query)
    # returns tuples
    rows = cursor.fetchall()
    assert len(rows) == 2
    numeric_cols = [i for i in range(len(columns)) if column_types[columns[i]] != 'text']
    v1 = [rows[0][i] for i in numeric_cols]
    v2 = [rows[1][i] for i in numeric_cols]
    print(v1, v2)

    all_mins = cursor.execute("SELECT * from dramas WHERE id = 'min'").fetchall()[0] #is this tuple or [tuple]?
    all_maxs = cursor.execute("SELECT * from dramas WHERE id = 'max'").fetchall()[0] #is this tuple or [tuple]?
    mins = [all_mins[i] for i in numeric_cols]
    maxs = [all_maxs[i] for i in numeric_cols]

    assert len(mins) == len(maxs) and len(maxs) == len(v1) and len(v1) == len(v2)

    # rescale values based on maxima and minima
    v1 = normalize(v1, mins, maxs)
    v2 = normalize(v2, mins, maxs)
    print(v1, v2)
    dist = math.dist(v1, v2)
    # normalize so that 0 < sim < 1
    sim = 1 - (dist / math.sqrt(len(numeric_cols)))
    return sim

def normalize(v: list, mins: list, maxs: list):
    v_norm = []
    for i in range(len(v)):
        v_norm.append((v[i] - mins[i])/ (maxs[i] - mins[i]))
    return v_norm