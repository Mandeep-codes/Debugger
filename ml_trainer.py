import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib

def train_model():
    df = pd.read_csv('error_data.csv')
    X = df['error_text']
    y = df['error_type']

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X, y)

    joblib.dump(model, 'error_classifier.joblib')



if  __name__ == "__main__":
    train_model()
