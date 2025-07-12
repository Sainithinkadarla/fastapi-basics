# pip install transformers
from transformers import pipeline

def get_model():
    return pipeline("sentiment-analysis")

