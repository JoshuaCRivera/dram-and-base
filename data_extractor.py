import os
import csv
import xml.etree.ElementTree as ET
import sentiment_prediction as sp

directory = 'tei/'
csv_file = 'dialogue_data.csv'

with open(csv_file, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(['Filename', 'Speaker', 'Text', 'Line Number', 'Emotion', 'Polarity'])

    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            xml_file = os.path.join(directory, filename)

            tree = ET.parse(xml_file)
            root = tree.getroot()

            namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}

            dialogue_lines = root.findall('.//tei:sp', namespace)

            previous_speaker = None
            line_number = 1

            for dialogue in dialogue_lines:
                speaker_element = dialogue.find('tei:speaker', namespace)
                if speaker_element is not None and speaker_element.text is not None:
                    speaker = speaker_element.text.strip()
                else:
                    speaker = ''

                for line in dialogue.findall('.//tei:p', namespace):
                    text = ' '.join(line.itertext()).replace('\n', ' ').strip()

                    for tag in line.findall('.//*'):
                        tag_text = ''.join(tag.itertext())
                        text = text.replace(tag_text, '')

                    emotion = sp.predict_emotion(text)
                    polarity = sp.predict_polarity(text)
                    print(filename)
                    print(text)
                    print(emotion)
                    print(polarity)
                    print(line_number)

                    writer.writerow([filename, speaker, text, line_number, emotion, polarity])

                    line_number += 1

                previous_speaker = speaker
