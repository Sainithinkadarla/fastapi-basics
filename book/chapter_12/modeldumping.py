from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

categories = [
"soc.religion.christian",
"talk.religion.misc",
"comp.sys.mac.hardware",
"sci.crypt",
]

news_train = fetch_20newsgroups(subset="train", categories= categories, random_state=0)
news_test = fetch_20newsgroups(subset="test", categories=categories, random_state=0)

model = make_pipeline(TfidfVectorizer(), 
                      MultinomialNB())

model.fit(news_train.data, news_train.target)

model_target_tuple = (model, news_train.target_names)
joblib.dump(model_target_tuple, "model.joblib")