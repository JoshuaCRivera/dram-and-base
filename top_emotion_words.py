import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

def remove_stop_words(text):
    stop_words = set(stopwords.words('german'))
    
    # Simple catch for some dialectal spellings
    stop_words.update(set([word[:-1] for word in stop_words]))
    
    tokens = word_tokenize(text, language='german')
    filtered_tokens = [token for token in tokens if token.lower() not in stop_words and len(token) > 2]
    
    return ' '.join(filtered_tokens)

def get_top_words(filename):
    df = pd.read_csv(filename).dropna(subset=['Text'])

    df['Text'] = df['Text'].apply(remove_stop_words)

    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df['Text'])

    feature_names = vectorizer.get_feature_names_out()

    emotion_tags = df['Emotion'].unique()
    for tag in emotion_tags:
        concatenated_text = ' '.join(df[df['Emotion'] == tag]['Text'])

        tfidf_vector = vectorizer.transform([concatenated_text])

        tfidf_scores = tfidf_vector.toarray()[0]

        top_word_indices = np.argsort(tfidf_scores)[-15:][::-1]

        top_words = [feature_names[idx] for idx in top_word_indices]

        print(f"Emotion Tag: {tag}")
        print(f"Top 15 Most Informative Emotion Words: {top_words}")
        print()

get_top_words('dialogue_data.csv')

