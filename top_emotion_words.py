import pandas as pd
import numpy as np
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

def get_top_words(filename):
    nlp = spacy.load('de_core_news_sm')
    
    df = pd.read_csv(filename).dropna(subset=['Text'])
    
    stopwords_german = nlp.Defaults.stop_words
    
    # Simple catch for some dialectal spellings
    stopwords_german.update([word[:-1] for word in nlp.Defaults.stop_words])
    
    df['Text'] = df['Text'].apply(lambda x: ' '.join([token.text.lower() for token in nlp(x) if token.text.lower() not in stopwords_german]))
    
    vectorizer = TfidfVectorizer(max_features=1000)
    tfidf_matrix = vectorizer.fit_transform(df['Text'])
    
    feature_names = vectorizer.get_feature_names_out()
    
    emotion_tags = df['Emotion'].unique()
    for tag in emotion_tags:
        concatenated_text = ' '.join(df[df['Emotion'] == tag]['Text'])
        
        tfidf_vector = vectorizer.transform([concatenated_text])
        
        tfidf_scores = tfidf_vector.toarray()[0]
        
        top_word_indices = np.argsort(tfidf_scores)[-10:][::-1]
        
        top_words = [feature_names[idx] for idx in top_word_indices]
        
        print(f"Emotion Tag: {tag}")
        print(f"Top 10 Most Informative Emotion Words: {top_words}")
        print()
        
get_top_words('dialogue_data.csv')
