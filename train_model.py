import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import joblib

df = pd.read_csv("spam_dataset.csv")

pipeline = Pipeline([("tfidf", TfidfVectorizer()), ("nb", MultinomialNB())])
pipeline.fit(df["text"], df["label"])

joblib.dump(pipeline, "model.joblib")
print("Done; used", len(df), "rows")
