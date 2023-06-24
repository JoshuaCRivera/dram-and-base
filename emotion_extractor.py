import os
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

                    if title not in emotion_data:
                        emotion_data[title] = []
                    print(title)
                    emotion_data[title].append({
                        'Speaker': speaker,
                        #'Text': text,
                        'Line Number': line_number,
                        'Emotion': emotion,
                        'Polarity': polarity
                    })

                    line_number += 1

                previous_speaker = speaker

    return emotion_data
 
directory = 'tei/'
print(emotion_extractor(directory))
