import csv

def count_emotions_percentage_per_title(file_path):
    emotions_per_title = {}

    # Open the CSV file
    with open(file_path, 'r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file, delimiter='\t')

        # Skip the header row
        next(reader)

        # Iterate over each row in the CSV file
        for row in reader:
            title = row[0]      # Extract the title from the row
            emotion = row[4]    # Extract the emotion from the row

            # Initialize a dictionary for each title if it doesn't exist
            if title not in emotions_per_title:
                emotions_per_title[title] = {'Freude': 0, 'Leid': 0, 'Ärger': 0, 'Verehrung': 0, 'Liebe': 0, 'Angst': 0, 'Abscheu': 0}


            # Initialize the emotion count for each title if it doesn't exist
            # if emotion not in emotions_per_title[title]:
            #     emotions_per_title[title][emotion] = 0

            # Increment the count for the emotion for the specific title
            emotions_per_title[title][emotion] += 1

        # Calculate the percentage of emotions for each title
        for title, emotions in emotions_per_title.items():
            total_emotions = sum(emotions.values())  # Calculate the total emotion count
            for emotion in emotions:
                # Calculate the percentage of each emotion for the specific title
                emotions[emotion] = emotions[emotion] / total_emotions * 100

    # Return the dictionary containing emotions percentage per title
    return emotions_per_title

# Define the file path of the CSV file
file_path = 'dialogue_data.csv'

#print(count_emotions_percentage_per_title(file_path))

