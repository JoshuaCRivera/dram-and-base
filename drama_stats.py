import xml.etree.ElementTree as ET
import os
import db_handling

drama_stats = {}

for drama_file in os.listdir('data'):
    tree = ET.parse(os.path.join('data', drama_file))
    root = tree.getroot()

    id_no = root.find('.//{http://www.tei-c.org/ns/1.0}idno').text
    print(id_no)

    title_stmt = root.find('.//{http://www.tei-c.org/ns/1.0}fileDesc/{http://www.tei-c.org/ns/1.0}titleStmt')
    print(title_stmt.findall('./*'))
    title = title_stmt.find('./{http://www.tei-c.org/ns/1.0}title[@type="main"]').text
    subtitle = title_stmt.find('./{http://www.tei-c.org/ns/1.0}title[@type="sub"]').text
    author = title_stmt.findall('.//{http://www.tei-c.org/ns/1.0}author/{http://www.tei-c.org/ns/1.0}persName/*')
    author = " ".join([author_part.text for author_part in author])

    # currently getting publication, not premiere
    year = root.find('.//{http://www.tei-c.org/ns/1.0}standOff//{http://www.tei-c.org/ns/1.0}event[@type="print"]').get('when')

    num_scenes = len(root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="scene"]'))
    num_lines = len(root.findall('.//{http://www.tei-c.org/ns/1.0}div[@type="scene"]//{http://www.tei-c.org/ns/1.0}p'))

    num_stage_dirs = len(root.findall('.//{http://www.tei-c.org/ns/1.0}stage'))

    drama_stats[id_no] = {"id": id_no, "title": title, "author": author, "year": year, "num_scenes": num_scenes, "num_lines": num_lines,
                          "num_stage_dirs": num_stage_dirs,  }


print(drama_stats)
db_handling.create_drama_db(drama_stats)
print(db_handling.similarity(drama1="Q214310", drama2="Q68117"))