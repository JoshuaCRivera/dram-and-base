import xml.etree.ElementTree as ET

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
            dialogue = ' '.join([line.text.strip() for line in sp.findall('tei:l', namespace)])
        except:
            continue
            print("cont")
        
        length = len(dialogue)

        if length > longest_length:
            longest_length = length
            longest_speaker = speaker
            longest_line = dialogue

        if length < shortest_length:
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

# Example:
filename = "tei/sachs-ein-comedi-von-dem-reichen-sterbenden-menschen-der-hecastus-genannt.xml"
#print(character_stats(filename))



