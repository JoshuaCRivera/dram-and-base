import xml.etree.ElementTree as ET
import os

def get_all_character_stats():
    character_stats = {}

    for drama_file in os.listdir('tei'):
        tree = ET.parse(os.path.join('tei', drama_file))
        root = tree.getroot()
        namespace = {'tei': 'http://www.tei-c.org/ns/1.0', 'xml': 'http://www.w3.org/XML/1998/namespace'}

        title = root.find('.//tei:titleStmt/tei:title[@type="main"]', namespace).text.strip().replace("'","")

        id_no = drama_file[:-4] # root.find('.//{http://www.tei-c.org/ns/1.0}idno').text
        #print(id_no)

        all_characters = []
        for person in root.findall(".//tei:person", namespace) + root.findall(".//tei:personGrp", namespace):
            char_id = id_no + "-" + person.get('{http://www.w3.org/XML/1998/namespace}id')
            all_characters.append(person.get('{http://www.w3.org/XML/1998/namespace}id'))
            #print(char_id)
            name_options = person.findall('.//tei:persName', namespace) + person.findall('.//tei:name', namespace)
            name = name_options[0].text.strip().replace("'","") # Strip leading and trailing whitespace 
            gender = person.get('sex', 'unknown')

            if not name:  # check for empty characters
                print(char_id, name)
                raise Exception("empty character?")
            
            character_stats[char_id] = {"id": char_id, "name": name, "drama": title, "drama_id": id_no, "gender": gender,
                                        "num_lines": 0, "num_scenes": 0,
                                        "len_longest_line": 0, "len_shortest_line": 10000,
                                        "relations": ""}

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
            print("no scenes")
            for character in all_characters:
                character_stats[id_no + '-' + character]["num_scenes"] = 1

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


        for sp in root.findall('.//tei:sp', namespace):
            try:
                speakers = sp.get('who').split()
            except:
                continue
            for speaker_r in speakers:
                speaker = id_no + '-' + speaker_r.removeprefix('#')
                if speaker not in character_stats:
                    continue
                try:
                    dialogue = ' '.join([line.text.strip() for line in sp.findall('.//tei:l', namespace) + sp.findall('.//tei:p', namespace)])
                except:
                    #hm = sp.findall('.//tei:p', namespace)[0]
                    #print("empty l or p?", speakers, hm.findall('../*'))
                    #TODO still a mystery
                    continue
                
                length = len(dialogue)

                if length > character_stats[speaker]["len_longest_line"]:
                    character_stats[speaker]["len_longest_line"] = length

                if 0 < length < character_stats[speaker]["len_shortest_line"]: 
                    character_stats[speaker]["len_shortest_line"] = length

                character_stats[speaker]['num_lines'] += 1

        for charmander in all_characters:
            if character_stats[id_no + '-' + charmander]["len_shortest_line"] == 10000:
                character_stats[id_no + '-' + charmander]["len_shortest_line"] == 0
        #print(character_stats)
    return character_stats


# Example:
#get_all_character_stats()
#filename = "tei/sachs-ein-comedi-von-dem-reichen-sterbenden-menschen-der-hecastus-genannt.xml"
#print(character_stats(filename))

#####old version##########
'''
def character_stats(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}

    title = root.find('.//tei:titleStmt/tei:title[@type="main"]', namespace).text.strip()

    id_no = root.find('.//{http://www.tei-c.org/ns/1.0}idno').text

    characters = []
    for name in root.findall(".//tei:persName", namespace):
        character = name.text.strip()  # Strip leading and trailing whitespace
        if character:  # Skip empty characters
            characters.append(character)

    profile_desc = root.find(".//tei:profileDesc", namespace)
    relations = profile_desc.findall(".//tei:relation", namespace)

    relationships = []
    for relation in relations:
        relationship_type = relation.attrib["name"]
        mutual = relation.attrib.get("mutual", "").split()
        active = relation.attrib.get("active", "").split()
        passive = relation.attrib.get("passive", "").split()

        relationships.append((relationship_type, mutual, active, passive))

    longest_length = 0
    longest_speaker = ''
    longest_line = ''

    shortest_length = 1000
    shortest_speaker = ''
    shortest_line = ''

    speaker_counts = {}

    for sp in root.findall('.//tei:sp', namespace):
        try:
            speaker = sp.find('tei:speaker', namespace).text
            dialogue = ' '.join([line.text.strip() for line in sp.findall('.//tei:l', namespace) + sp.findall('.//tei:p', namespace)])
        except:
            continue
            print("cont")
        
        length = len(dialogue)

        if length > longest_length:
            longest_length = length
            longest_speaker = speaker
            longest_line = dialogue

        if 0 < length < shortest_length:
            shortest_length = length
            shortest_speaker = speaker
            shortest_line = dialogue

        if speaker in speaker_counts:
            speaker_counts[speaker] += 1
        else:
            speaker_counts[speaker] = 1

    character_stats = {
        "id": id_no,
        "title": title,
        "num_characters": len(sorted(characters)),
        #"speaker_counts": {speaker: count for speaker, count in sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True)},
        #"relationships": relationships,
        #"longest_dialogue": {
        #   "speaker": longest_speaker,
            "longest_dialogue": longest_length,
            #"line": longest_line
        #},
        #"shortest_dialogue": {
        #    "speaker": shortest_speaker,
            "shortest_dialogue": shortest_length,
            #"line": shortest_line
        #}
    }

    return character_stats
'''


