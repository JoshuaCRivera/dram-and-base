from drama_stats import get_all_drama_stats
from character_data import get_all_character_stats, update_char_stats
#from german_drama_emotion_classifier import *
from db_handling import *
from querying import *
import os

if not "drama_base.db" in os.listdir():
    # extracts all the info about the drama with XPath
    dramas = get_all_drama_stats()
    # add emotion info

    # creates table dramas in SQLite database
    create_drama_db(dramas)

    # extracts all the info about the characters with XPath
    characters = get_all_character_stats()
    characters = update_char_stats(characters, dramas)

    # creates table characters in SQLite database
    create_characters_db(characters)

print(len(query(f"SELECT COUNT(*) FROM characters WHERE name LIKE '%Faust%' AND characters.main_char = 'Yes' GROUP BY drama_id")))
print(query(f"SELECT characters.drama FROM characters WHERE characters.name LIKE '%König%'"))
# add db queries and similarity queries here
#print(top_k_most_similar("gerhaeuser-der-moloch"))
#print(query("SELECT d.title, d.id FROM dramas AS d WHERE d.id NOT IN (SELECT c.drama_id FROM characters AS c WHERE c.gender = 'MALE') AND d.id NOT LIKE 'min' AND d.id NOT LIKE 'max'"))

