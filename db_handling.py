import sqlite3

def create_drama_db(dramas_dict: dict):
    connection = sqlite3.connect('drama_base.db')
    cursor = connection.cursor()

    # getting column names and types, translating those to sql (ugly)
    columns = list(list(dramas_dict.values())[0].keys())
    type_dict = {"<class 'int'>": "integer", "<class 'str'>": "text", "<class 'float'>": "real"}
    column_types = {col: type_dict[str(type(list(dramas_dict.values())[0][col]))] for col in columns}
    print(column_types)

    #creating table
    columns_str = ", ".join(f"{col} {column_types[col]}" for col in columns)
    create_query_d = "CREATE TABLE dramas(id text PRIMARY KEY, " + columns_str + ")"
    print(create_query_d)
    cursor.execute(create_query_d)

    # adding drama data to table
    for id, drama in dramas_dict.items():
        # this is a bad way to ensure text comes in ''
        insert_query_d = f"INSERT INTO dramas VALUES('{id}'"
        for col in columns:
            if column_types[col] == 'text':
                insert_query_d += f", '{drama[col]}'"
            else:
                insert_query_d += f", {drama[col]}"
        insert_query_d += ")"
        print(insert_query_d)
        cursor.execute(insert_query_d)
        connection.commit()


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
        