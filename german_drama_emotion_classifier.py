import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import pickle

# Training data comes from https://dfg-spp-cls.github.io/projects_en/2020/01/24/TP-Emotions_in_Drama/
data = pd.read_csv('large_emotions_filtered_withNoAnnotations.csv')
data = data[(data['tag_type'] != 'no_annotation') & (data['tag_type'] != 'Emotionale Bewegtheit')]

X = data['text']
y_emotion = data['tag_type']
y_polarity = data['polarity']

X_train, X_test, y_train_emotion, y_test_emotion, y_train_polarity, y_test_polarity = train_test_split(
    X, y_emotion, y_polarity, test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

model_emotion = LinearSVC()
model_emotion.fit(X_train, y_train_emotion)

y_pred_emotion = model_emotion.predict(X_test)
print("Emotion Classification Report:")
print(classification_report(y_test_emotion, y_pred_emotion, zero_division=1))

with open('emotion_model.pkl', 'wb') as f:
    pickle.dump(model_emotion, f)

model_polarity = LinearSVC()
model_polarity.fit(X_train, y_train_polarity)

y_pred_polarity = model_polarity.predict(X_test)
print("Polarity Classification Report:")
print(classification_report(y_test_polarity, y_pred_polarity, zero_division=1))

with open('polarity_model.pkl', 'wb') as f:
    pickle.dump(model_polarity, f)

# Save the vectorizer
with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

