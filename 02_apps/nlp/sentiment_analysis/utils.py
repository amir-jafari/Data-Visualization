import streamlit as st
import re
import nltk
from textblob import TextBlob


def get_txt():
    txt = st.text_area(
        "Text to analyze",
        "It was the best of times, it was the worst of times, it was the age of "
        "wisdom, it was the age of foolishness, it was the epoch of belief, it "
        "was the epoch of incredulity, it was the season of Light, it was the "
        "season of Darkness, it was the spring of hope, it was the winter of "
        "despair, (...)",
    )

    st.write(f'You wrote {len(txt)} characters.')
    return txt


def text_pre_processing(text, flg_stemm=False, flg_lemm=True, lst_stopwords=None):
    text = re.sub(r'[^\w\s]', '', str(text).lower().strip())
    lst_text = text.split()
    if lst_stopwords is not None:
        lst_text = [word for word in lst_text if word not in lst_stopwords]
    if flg_stemm == True:
        ps = nltk.stem.porter.PorterStemmer()
        lst_text = [ps.stem(word) for word in lst_text]
    if flg_lemm == True:
        lem = nltk.stem.wordnet.WordNetLemmatizer()
        lst_text = [lem.lemmatize(word) for word in lst_text]
    text = " ".join(lst_text)
    return text


def analyze_sentiment(text):
    # Create a TextBlob object
    testimonial = TextBlob(text)
    # print('testimonial', testimonial.sentiment)
    # This will return a namedtuple of the form Sentiment(polarity, subjectivity)
    # Polarity is a float within the range [-1.0, 1.0]
    # Subjectivity is a float within the range [0.0, 1.0] where 0.0 is very objective and 1.0 is very subjective
    return testimonial.sentiment
