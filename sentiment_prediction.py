import pickle

# Load the models
with open('emotion_model.pkl', 'rb') as f:
    model_emotion = pickle.load(f)

with open('polarity_model.pkl', 'rb') as f:
    model_polarity = pickle.load(f)

with open('vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

def predict_emotion(sentence):
    sentence_vectorized = vectorizer.transform([sentence])
    emotion_prediction = model_emotion.predict(sentence_vectorized)
    return emotion_prediction[0]

def predict_polarity(sentence):
    sentence_vectorized = vectorizer.transform([sentence])
    polarity_prediction = model_polarity.predict(sentence_vectorized)
    return polarity_prediction[0]

# Example usage
#sentence = "Das Stück ist wirklich großartig"
#print(sentence)
#print("Predicted emotion:", predict_emotion(sentence))
#print("Predicted polarity:", predict_polarity(sentence))

