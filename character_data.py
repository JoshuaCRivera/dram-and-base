import xml.etree.ElementTree as ET
import os, re

'''
Iterates through all character in all dramas, collects some basic info and calculates some statistics about each.
Outputs a dictionary id:character_stats of the shape db_handling.create_character_db wants it
'''
def get_all_character_stats(corpus='tei'):
    character_stats = {}

    for drama_file in os.listdir(corpus):
        tree = ET.parse(os.path.join(corpus, drama_file))
        root = tree.getroot()
        namespace = {'tei': 'http://www.tei-c.org/ns/1.0', 'xml': 'http://www.w3.org/XML/1998/namespace'}

        title = " ".join(root.find('.//tei:titleStmt/tei:title', namespace).itertext()).strip().replace("'","") #main should always be first, [@type="main"] removed for compatibility with swe
        id_no = drama_file[:-4] # remove .xml

        # initialize basic stats for all characters
        all_characters = []
        for person in root.findall(".//tei:particDesc//tei:person", namespace) + root.findall(".//tei:particDesc//tei:personGrp", namespace): #CHANGED added particDesc
            char_id = id_no + "-" + person.get('{http://www.w3.org/XML/1998/namespace}id')
            all_characters.append(person.get('{http://www.w3.org/XML/1998/namespace}id'))

            name_options = person.findall('.//tei:persName', namespace) + person.findall('.//tei:name', namespace)
            
            if len(name_options) > 0: #CHANGED adapted for swe
                name = name_options[0].text.strip().replace("'","")
            else: #characters without names, appearantly 
                #print(char_id)
                name = person.get('{http://www.w3.org/XML/1998/namespace}id')
            gender = person.get('sex', 'unknown')

            if not name:  # check for empty characters
                print(char_id, name)
                raise Exception("empty character?")
            
            character_stats[char_id] = {"id": char_id, "name": name, "drama": title, "drama_id": id_no, "gender": gender,
                                        "num_lines": 0, "num_scenes": 0, "percentage_lines": 0., "main_char": "No",
                                        "len_longest_line": 0, "len_shortest_line": 10000,
                                        "relations": "", "dead": "No"}

        # number of scenes 
        if root.findall('.//tei:div[@type="scene"]', namespace):
            all_scenes = root.findall('.//tei:div[@type="scene"]', namespace)
        else:
            all_scenes = root.findall('.//tei:div[@type="act"]', namespace)

        for scene in all_scenes:
            for character in all_characters:
                if scene.find(f".//tei:sp[@who='#{character}']", namespace):
                    character_stats[id_no + '-' + character]["num_scenes"] += 1
        if len(all_scenes) == 0:
            #print("no scenes")
            for character in all_characters:
                character_stats[id_no + '-' + character]["num_scenes"] = 1

        # relations of the character
        relations = root.findall(".//tei:profileDesc//tei:relation", namespace)
        for relation in relations:
            relationship_type = relation.attrib["name"]

            if relation.get("mutual"):
                characters = relation.get("mutual").split()
                rel_string0 = f"({relationship_type} to {characters[0].removeprefix('#')})"
                character_stats[id_no + '-' + characters[1].removeprefix('#')]["relations"] += rel_string0
                rel_string1 = f"({relationship_type} to {characters[1].removeprefix('#')})"
                character_stats[id_no + '-' + characters[0].removeprefix('#')]["relations"] += rel_string1
            else:
                active = relation.get('active').split()
                for character in active:
                    rel_string = f"({relationship_type} to {relation.get('passive').removeprefix('#')})"
                    character_stats[id_no + '-' + character.removeprefix('#')]["relations"] += rel_string

        # iterate over each dialog turn
        for sp in root.findall('.//tei:sp', namespace):
            try:
                speakers = sp.get('who').split()
            except:
                continue
            for speaker_r in speakers:
                speaker = id_no + '-' + speaker_r.removeprefix('#')
                if speaker not in character_stats:
                    continue
                
                #for the "does a character die onstage" statistic
                #if sp.find('.//tei:stage', namespace):
                all_stage = " ".join([" ".join(s.itertext()) for s in sp.findall('.//tei:stage', namespace)])

                if re.search("(S|s)tirbt|\stot\s", all_stage):
                    character_stats[speaker]["dead"] = "Yes"
                
                # the issue is: we want the full text of a dialogue turn, but that's difficult if the p or l element has children.
                # xpath seemingly has no good way of doing this, so I'm using the children's tails + .text if available
                try:
                    full_lines = []
                    for line in sp.findall('.//tei:l', namespace) + sp.findall('.//tei:p', namespace):
                        full_line = ' '.join([c.tail.strip() for c in line if c.tail])
                        if line.text:
                            full_line = line.text + " " + full_line
                        full_lines.append(full_line)
                    dialogue = ' '.join(full_lines)
                    #dialogue = ' '.join([line.text.strip() for line in sp.findall('.//tei:l', namespace) + sp.findall('.//tei:p', namespace)])
                except:
                    #hm = sp.findall('.//tei:p', namespace)[0]
                    print(drama_file, " ".join(sp.itertext()))
                    #TODO still a mystery
                    raise Exception()
                    continue
                
                # for the "longest/shortest line" statistic
                length = len(dialogue)
                if length > character_stats[speaker]["len_longest_line"]:
                    character_stats[speaker]["len_longest_line"] = length

                if 0 < length < character_stats[speaker]["len_shortest_line"]: 
                    character_stats[speaker]["len_shortest_line"] = length

                character_stats[speaker]['num_lines'] += 1

        for char_name in all_characters:
            if character_stats[id_no + '-' + char_name]["len_shortest_line"] == 10000:
                character_stats[id_no + '-' + char_name]["len_shortest_line"] == 0
        #print(character_stats)
    return character_stats

'''
Secondary pass to add info (percentage of lines etc.) that require info from drama_stats, like percentage_lines
'''
def update_char_stats(characters, dramas):
    for character in characters.keys():
        char_stats = characters[character]
        total_lines = dramas[char_stats["drama_id"]]["num_lines"]
        total_chars = dramas[char_stats["drama_id"]]["num_characters"]
        num_scenes = dramas[char_stats["drama_id"]]["num_scenes"]
        char_stats["percentage_lines"] = char_stats["num_lines"]/total_lines
        # to count as main character: must have above average amount of lines and appear in at least a third of scenes
        if char_stats["percentage_lines"] > 1/total_chars and char_stats["num_scenes"] > 0.33 * num_scenes:
            char_stats["main_char"] = "Yes"
    return characters

