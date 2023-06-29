import csv

def count_emotions_percentage_per_title(file_path):
    emotions_per_title = {}

    with open(file_path, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter='\t')
        next(reader)

        for row in reader:
            title = row[0]
            emotion = row[4]

            if title not in emotions_per_title:
                emotions_per_title[title] = {'Freude' : 0, 'Leid': 0, 'Ärger': 0, 'Verehrung': 0, 'Liebe': 0, 'Angst': 0, 'Abscheu': 0}

            # if emotion not in emotions_per_title[title]:
            #     emotions_per_title[title][emotion] = 0

            emotions_per_title[title][emotion] += 1

        for title, emotions in emotions_per_title.items():
            total_emotions = sum(emotions.values())
            for emotion in emotions:
                emotions[emotion] = emotions[emotion] / total_emotions * 100

    return emotions_per_title

file_path = 'dialogue_data.csv'
#print(count_emotions_percentage_per_title(file_path))
