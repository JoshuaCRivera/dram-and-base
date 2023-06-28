import xml.etree.ElementTree as ET
import os, re
from db_handling import *



'''
Iterates through all dramas, collects some basic info and calculates some statistics about each.
Outputs a dictionary id:drama_stats of the shape db_handling.create_drama_db wants it
'''
def get_all_drama_stats():
    drama_stats = {}
    for drama_file in os.listdir('tei'):
        tree = ET.parse(os.path.join('tei', drama_file))
        root = tree.getroot()
        namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}


        id_no = drama_file[:-4] #root.find('.//{http://www.tei-c.org/ns/1.0}idno').text
        
        title_stmt = root.find('.//tei:fileDesc/tei:titleStmt', namespace)
        #print(title_stmt.findall('./*'))
        title = title_stmt.find('./{http://www.tei-c.org/ns/1.0}title[@type="main"]').text.replace("'","")
        #print(id_no)
        try:
            subtitle = title_stmt.find('./{http://www.tei-c.org/ns/1.0}title[@type="sub"]').text.replace("'","")
        except: 
            subtitle = ""

        if re.search("omödi|ustsp|osse|omisch|chert?z", subtitle):
            genre = "comedy"
        elif re.search("ragödi|rauer",subtitle):
            genre = "tragedy"
        else:
            genre = "unknown"
        author = title_stmt.findall('.//{http://www.tei-c.org/ns/1.0}author/{http://www.tei-c.org/ns/1.0}persName/*')
        author = " ".join([author_part.text for author_part in author]).replace("'","")

        # currently getting publication, not premiere
        if root.find('.//{http://www.tei-c.org/ns/1.0}standOff//{http://www.tei-c.org/ns/1.0}event[@type="print"]'):
            year = root.find('.//{http://www.tei-c.org/ns/1.0}standOff//{http://www.tei-c.org/ns/1.0}event[@type="print"]').get('when')
        elif root.find('.//{http://www.tei-c.org/ns/1.0}standOff//{http://www.tei-c.org/ns/1.0}event[@type="premiere"]'):
            year = root.find('.//{http://www.tei-c.org/ns/1.0}standOff//{http://www.tei-c.org/ns/1.0}event[@type="premiere"]').get('when')
        else:
            year = '1914'

        num_scenes = max(len(root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="scene"]')), len(root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="act"]')), 1)
        num_lines = len(root.findall('.//{http://www.tei-c.org/ns/1.0}sp//{http://www.tei-c.org/ns/1.0}p')) + len(root.findall('.//{http://www.tei-c.org/ns/1.0}sp//{http://www.tei-c.org/ns/1.0}l'))
        #num_lines = len(root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="scene"]//{http://www.tei-c.org/ns/1.0}p'))

        num_stage_dirs = len(root.findall('.//tei:stage', namespace))

        num_characters = len(root.findall(".//tei:persName", namespace))

        #character_data = character_stats(os.path.join('tei', drama_file))

        longest_length = 0
        shortest_length = 1000
        for sp in root.findall('.//tei:sp', namespace):
            try:
                dialogue = ' '.join([line.text.strip() for line in sp.findall('.//tei:l', namespace) + sp.findall('.//tei:p', namespace)])
            except:
                continue
            length = len(dialogue)
            if length > longest_length:
                longest_length = length
            if 0 < length < shortest_length:
                shortest_length = length

        stats = {"id": id_no, "title": title, "subtitle": subtitle, "author": author, "year": year, "genre": genre,
                            "num_scenes": num_scenes, "num_lines": num_lines, "num_stage_dirs": num_stage_dirs, 
                            "num_characters": num_characters, "longest_dialogue": longest_length, "shortest_dialogue": shortest_length}

        drama_stats[id_no] = stats

    print(len(drama_stats.keys()))
    return drama_stats

#drama_stats = get_all_drama_stats()
#print(drama_stats)
#create_drama_db(drama_stats)
#v1 = drama_vector("Die Grille")
#v2 = average_of_all("num_scenes > 10")
#print(similarity(v1, v2))