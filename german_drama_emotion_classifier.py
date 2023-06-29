import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import pickle

# Read the training data from CSV file
data = pd.read_csv('large_emotions_filtered_withNoAnnotations.csv')

# Filter out unwanted tag types
data = data[(data['tag_type'] != 'no_annotation') & (data['tag_type'] != 'Emotionale Bewegtheit')]

# Reduce the different categories to just 7 emotions that are better distributed
data['tag_type'] = data['tag_type'].replace({'Abscheu': 'Abscheu',
                                             'Ärger': 'Ärger',
                                             'Angst': 'Angst',
                                             'Verzweiflung': 'Angst',
                                             'Freude': 'Freude',
                                             'Lust': 'Freude',
                                             'Freundschaft': 'Freude',
                                             'Verehrung': 'Verehrung',
                                             'Leid': 'Leid',
                                             'Mitleid': 'Leid',
                                             'Liebe': 'Liebe',
                                             'Schadenfreude': 'Freude'})

X = data['text']
y_emotion = data['tag_type']
y_polarity = data['polarity']

# Split the data into training and testing sets
X_train, X_test, y_train_emotion, y_test_emotion, y_train_polarity, y_test_polarity = train_test_split(
    X, y_emotion, y_polarity, test_size=0.2, random_state=42
)

# Create a TfidfVectorizer and transform the text data
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Train the emotion classification model
model_emotion = LinearSVC()
model_emotion.fit(X_train, y_train_emotion)

# Predict the emotion labels for the test set
y_pred_emotion = model_emotion.predict(X_test)

# Print the emotion classification report
print("Emotion Classification Report:")
print(classification_report(y_test_emotion, y_pred_emotion, zero_division=1))

# Save the emotion classification model
with open('emotion_model.pkl', 'wb') as f:
    pickle.dump(model_emotion, f)

# Train the polarity classification model
model_polarity = LinearSVC()
model_polarity.fit(X_train, y_train_polarity)

# Predict the polarity labels for the test set
y_pred_polarity = model_polarity.predict(X_test)

# Print the polarity classification report
print("Polarity Classification Report:")
print(classification_report(y_test_polarity, y_pred_polarity, zero_division=1))

# Save the polarity classification model
with open('polarity_model.pkl', 'wb') as f:
    pickle.dump(model_polarity, f)

# Save the vectorizer
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

