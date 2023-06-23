import xml.etree.ElementTree as ET

def character_stats(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}

    characters = []
    for name in root.findall(".//tei:persName", namespace):
        characters.append(name.text)

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

    shortest_length = 100
    shortest_speaker = ''
    shortest_line = ''

    speaker_counts = {}

    for sp in root.findall('.//tei:sp', namespace):
        speaker = sp.find('tei:speaker', namespace).text
        dialogue = ' '.join([line.text.strip() for line in sp.findall('tei:l', namespace)])

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

    print("Named Characters:")
    for c in sorted(characters):
        print(c)
    print()

    print("Speaker Counts:")
    for speaker, count in sorted(speaker_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{speaker}: {count}")
    print()

    print("Relationships:")
    for relationship, mutual, active, passive in relationships:
        print("Relationship:", relationship)
        print("Mutual:", mutual)
        print("Active:", active)
        print("Passive:", passive)
        print()

    print("Speaker of longest dialogue:", longest_speaker)
    print("Length of longest dialogue:", longest_length)
    # print("Longest dialogue:", longest_line)
    print()

    print("Speaker of shortest dialogue:", shortest_speaker)
    print("Length of shortest dialogue:", shortest_length)
    # print("Shortest dialogue:", shortest_line)

# Example:
filename = "tei/sachs-ein-comedi-von-dem-reichen-sterbenden-menschen-der-hecastus-genannt.xml"
character_stats(filename)



