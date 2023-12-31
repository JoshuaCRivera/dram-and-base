import sqlite3
import math
import numpy as np
'''
This file implements methods to create query the drama database and to calculate similaritites.
'''

columns = ['id', 'title', 'subtitle', 'author', 'year', 'genre', 'setting', 'num_scenes', 'num_lines', 'num_stage_dirs', 'num_characters', 'longest_dialogue', 'shortest_dialogue', 'Freude', 'Leid', 'Ärger', 'Verehrung', 'Liebe', 'Angst', 'Abscheu']
column_types = {'id': 'text', 'title': 'text', 'subtitle': 'text', 'author': 'text', 'year': 'text', 'genre': 'text', 'setting': 'text', 
                'num_scenes': 'integer', 'num_lines': 'integer', 'num_stage_dirs': 'integer', 'num_characters': 'integer', 
                'longest_dialogue': 'integer', 'shortest_dialogue': 'integer', 
                'Freude': 'real', 'Leid': 'real', 'Ärger': 'real', 'Verehrung': 'real', 'Liebe': 'real', 'Angst': 'real', 'Abscheu': 'real'}
numeric_cols = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

'''
Creates a SQLite database and in it a table dramas
Input: a dictionary representing a list of dramas, each value in the dict is a dictionary representing entries as column: value.
Also appends a line each to the table for minima and maxima in the numeric columns.
'''
def create_drama_db(dramas_dict: dict):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()

    # getting column names and types, translating those to sql (ugly)
    global columns, numeric_cols, column_types
    #print(list(dramas_dict.values())[:3])
    columns = list((list(dramas_dict.values())[0].keys()))
    print(columns)
    type_dict = {"<class 'int'>": "integer", "<class 'str'>": "text", "<class 'float'>": "real"}
    column_types = {col: type_dict[str(type(list(dramas_dict.values())[0][col]))] for col in columns}
    #print(column_types)
    numeric_cols = [i for i in range(len(columns)) if column_types[columns[i]] != 'text']
    #print(numeric_cols)

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
            print(insert_query_d)
            raise Exception("Couldn't add drama")
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
    print("number of dramas: ", len(dramas_dict))

'''
Creates table characters in the db 
Input: A dictionary where each value is a dict that represents the column:vallue entries for one character
'''
def create_characters_db(char_dict):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()
    columns = list(list(char_dict.values())[0].keys())
    type_dict = {"<class 'int'>": "integer", "<class 'str'>": "text", "<class 'float'>": "real"}
    column_types = {col: type_dict[str(type(list(char_dict.values())[0][col]))] for col in columns}
    #print(column_types)

    # create table
    columns_str = ", ".join(f"{col} {column_types[col]}" for col in columns[1:])
    create_query_c = "CREATE TABLE characters(id text PRIMARY KEY, " + columns_str + ")"
    #print(create_query_c)
    cursor.execute(create_query_c)

    # adding character data to table
    for character in char_dict.values():
    
        entries = []
        for col in columns:
            if column_types[col] == 'text':
                entries.append(f"'{character[col]}'")
            else:
                entries.append( f"{character[col]}")

        insert_query_c = f"INSERT INTO characters VALUES(" + ", ".join(entries) + ")"
        #print(insert_query_c)
        try:
            cursor.execute(insert_query_c)
        except:
            print(insert_query_c)
            raise Exception()
        connection.commit()
    connection.close()
    print("number of characters: ", len(char_dict))

'''
Takes drama ID or name and returns normalized drama vector for similarity
'''
def drama_vector(drama: str):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()
    query = f"SELECT * from dramas WHERE id = '{drama}' OR title = '{drama}'"
    cursor.execute(query)
    # returns tuples
    rows = cursor.fetchall()
    assert len(rows) == 1

    # these are column indices
    #numeric_cols = [i for i in range(len(columns)) if column_types[columns[i]] != 'text']
    v = [rows[0][i] for i in numeric_cols]

    all_mins = cursor.execute("SELECT * from dramas WHERE id = 'min'").fetchall()[0] #is this tuple or [tuple]?
    all_maxs = cursor.execute("SELECT * from dramas WHERE id = 'max'").fetchall()[0] #is this tuple or [tuple]?
    mins = [all_mins[i] for i in numeric_cols]
    maxs = [all_maxs[i] for i in numeric_cols]

    assert len(mins) == len(maxs) and len(maxs) == len(v)

    # rescale values based on maxima and minima
    v = normalize(v, mins, maxs)
    return v

'''
takes in a condition in SQL syntax and returns the average of all dramas fulfilling that condition 
as a normalized numeric vector 
'''
def average_of_all(condition:str):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()
    query = "SELECT * from dramas WHERE " + condition
    rows = cursor.execute(query).fetchall()
    n = len(rows)
    #numeric_cols = [i for i in range(len(columns)) if column_types[columns[i]] != 'text']
    all_mins = cursor.execute("SELECT * from dramas WHERE id = 'min'").fetchall()[0] #is this tuple or [tuple]?
    all_maxs = cursor.execute("SELECT * from dramas WHERE id = 'max'").fetchall()[0] #is this tuple or [tuple]?
    mins = [all_mins[i] for i in numeric_cols]
    maxs = [all_maxs[i] for i in numeric_cols]
    
    avg_vector = []
    for i in numeric_cols:
        avg_vector.append(sum([row[i] for row in rows]) / n)
    avg_vector = normalize(avg_vector, mins=mins, maxs=maxs) #TODO maybe first norm, then avg?
    return avg_vector

'''
auxiliary function: normalizes a vector to the range (0, 1) based on the maximum and minimum values 
'''
def normalize(v: list, mins: list, maxs: list):
    v_norm = []
    for i in range(len(v)):
        v_norm.append((v[i] - mins[i])/ (maxs[i] - mins[i]))
    return v_norm
