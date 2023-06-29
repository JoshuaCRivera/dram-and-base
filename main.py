from drama_stats import get_all_drama_stats
from character_data import get_all_character_stats
#from german_drama_emotion_classifier import *
from db_handling import *
import os

if not "drama_base.db" in os.listdir():
    # extracts all the info about the drama with XPath
    dramas = get_all_drama_stats()
    # add emotion info

    # creates table dramas in SQLite database
    create_drama_db(dramas)

    # extracts all the info about the characters with XPath
    characters = get_all_character_stats()

    # creates table dramas in SQLite database
    create_characters_db(characters)

# add db queries and similarity queries here
