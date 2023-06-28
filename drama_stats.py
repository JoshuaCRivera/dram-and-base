import xml.etree.ElementTree as ET
import os, re
from db_handling import *
from character_data import character_stats

drama_stats = {}

'''
Iterates through all dramas, collects some basic info and calculates some statistics about each.
Outputs a dictionary id:drama_stats of the shape db_handling.create_drama_db wants it
'''
def get_all_drama_stats():
    for drama_file in os.listdir('data'):
        tree = ET.parse(os.path.join('data', drama_file))
        root = tree.getroot()

        id_no = root.find('.//{http://www.tei-c.org/ns/1.0}idno').text
        print(id_no)

        title_stmt = root.find('.//{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}titleStmt')
        print(title_stmt.findall('./*'))
        title = title_stmt.find('./{http://www.tei-c.org/ns/1.0}title[@type="main"]').text
        subtitle = title_stmt.find('./{http://www.tei-c.org/ns/1.0}title[@type="sub"]').text
        if re.search("omödi|ustsp|osse|omisch|chert?z", subtitle):
            genre = "comedy"
        elif re.search("ragödi|rauer",subtitle):
            genre = "tragedy"
        else:
            genre = "unknown"
        author = title_stmt.findall('.//{http://www.tei-c.org/ns/1.0}author/{http://www.tei-c.org/ns/1.0}persName/*')
        author = " ".join([author_part.text for author_part in author])

        # currently getting publication, not premiere
        year = root.find('.//{http://www.tei-c.org/ns/1.0}standOff//{http://www.tei-c.org/ns/1.0}event[@type="print"]').get('when')

        num_scenes = len(root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="scene"]'))
        num_lines = len(root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="scene"]//{http://www.tei-c.org/ns/1.0}p'))

        num_stage_dirs = len(root.findall('.//{http://www.tei-c.org/ns/1.0}stage'))

        character_data = character_stats(drama_file)
        # add this

        drama_stats[id_no] = {"id": id_no, "title": title, "subtitle": subtitle, "author": author, "year": year, "genre": genre,
                            "num_scenes": num_scenes, "num_lines": num_lines, "num_stage_dirs": num_stage_dirs,  }
    return drama_stats

drama_stats = get_all_drama_stats()
print(drama_stats)
create_drama_db(drama_stats)
v1 = drama_vector("Die Grille")
v2 = average_of_all("num_scenes > 10")
print(similarity(v1, v2))