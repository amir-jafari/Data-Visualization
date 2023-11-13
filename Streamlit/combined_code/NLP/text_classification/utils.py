import re
import streamlit as st
import pandas as pd
import nltk
import seaborn as sns
import matplotlib.pyplot as plt


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


def upload_file(file_name):
    file = st.file_uploader(f"Choose the {file_name}", type="csv")

    if file is not None:
        df = pd.read_csv(file)
        st.write(df.head())
        return df


def get_text_label(df):
    options = st.multiselect(
        'Sequentially select the text and label columns',
        df.columns.tolist(),
        [])

    if len(options) == 2:
        st.write(f'Your text column is {options[0]}, and you label column is  {options[1]}')
        return options

    st.warning("You should pick up two columns")


def sidebar():
    with st.sidebar:
        genre = st.radio(
            "Choose your model",
            ["Naive Bayes", "LogisticRegression"],
            captions=["Use Naive Bayes to predict.", "Use logistic regression to predict."],
            index=None,
        )
        return genre


def draw(cm):
    sns.heatmap(cm, annot=True)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    st.pyplot(plt)


def download_file(df, model_name):
    st.write(f"Download The {model_name} result")
    st.download_button(
        label="Download DataFrame as CSV",
        data=df.to_csv(index=False),
        file_name="Test_predict.csv",
        mime="text/csv"
    )
