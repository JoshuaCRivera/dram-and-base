import pickle
import numpy as np

# Load the models
with open('emotion_model.pkl', 'rb') as f:
    model_emotion = pickle.load(f)

with open('polarity_model.pkl', 'rb') as f:
    model_polarity = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Run models
def predict_emotion(sentence):
    sentence_vectorized = vectorizer.transform([sentence])
    emotion_prediction = model_emotion.predict(sentence_vectorized)
    return emotion_prediction[0]

def predict_polarity(sentence):
    sentence_vectorized = vectorizer.transform([sentence])
    polarity_prediction = model_polarity.predict(sentence_vectorized)
    return polarity_prediction[0]
    
def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

#
def classify_text_emotion_polarity(text):
    # Vectorize the text
    text_vectorized = vectorizer.transform([text])

    # Predict the emotion
    emotion_scores = model_emotion.decision_function(text_vectorized)[0]
    emotion_probs = softmax(emotion_scores)
    emotions = model_emotion.classes_

    # Predict the polarity
    polarity_scores = model_polarity.decision_function(text_vectorized)[0]
    polarity_probs = softmax(polarity_scores)
    polarities = model_polarity.classes_

    # Create dictionaries with probabilities for emotions and polarities
    emotion_probabilities = {emotion: prob for emotion, prob in zip(emotions, emotion_probs)}
    polarity_probabilities = {polarity: prob for polarity, prob in zip(polarities, polarity_probs)}

    return emotion_probabilities, polarity_probabilities

