import os
import csv
import xml.etree.ElementTree as ET
import sentiment_prediction as sp

def emotion_extractor(directory):
    emotion_data = {}

    for filename in os.listdir(directory):
        if filename.endswith('.xml'):
            xml_file = os.path.join(directory, filename)

            tree = ET.parse(xml_file)
            root = tree.getroot()

            namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}

            title = root.find('.//tei:titleStmt/tei:title[@type="main"]', namespace).text.strip()
            id_no = root.find('.//tei:idno', namespace).text.strip()

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
                    
                    emotion_num, polarity_num = sp.classify_text_emotion_polarity(text)

                    if title not in emotion_data:
                        emotion_data[title] = []
                    print(title)
                    emotion_data[title].append({
                        'id_no': id_no,
                        'Speaker': speaker,
                        'Line Number': line_number,
                        'Emotion': emotion,
                        'Emotion Scores': emotion_num,
                        'Polarity': polarity,
                        'Polarity Scores': polarity_num,
                        'Text': text,
                    })

                    line_number += 1

                previous_speaker = speaker

    return emotion_data

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'id_no', 'Speaker', 'Line Number', 'Emotion','Emotion Scores', 'Polarity', 'Polarity Scores', 'Text',]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='\t')
        writer.writeheader()

        for title, lines in data.items():
            for line in lines:
                line['Title'] = title
                writer.writerow(line)

directory = 'tei/'
data = emotion_extractor(directory)
print(data)
save_to_csv(data, 'dialogue_data.csv')


