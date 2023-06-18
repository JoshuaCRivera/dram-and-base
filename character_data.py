import xml.etree.ElementTree as ET
import re

tree = ET.parse('data.xml')
root = tree.getroot()

speakers = root.findall('.//speaker')
persons = root.findall('.//person')
association = root.findall('.//listPerson//relation')

active_passive = []

for x in association:
    active_passive.append([x.attrib['active'], x.attrib['passive']])

character_names = []

for speaker in speakers:
    character_names.append(speaker.text)

total_characters = len(character_names)

print("Total unique dialogues:", total_characters)
unique_names = []
for name in persons:
    unique_names.append(name[0].text)
print("All character names:", unique_names)
print("All relationships, active -> passive:", active_passive)
