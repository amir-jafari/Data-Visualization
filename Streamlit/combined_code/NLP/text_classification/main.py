import streamlit as st

from sklearn import feature_extraction,  naive_bayes, pipeline
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.linear_model import LogisticRegression

import utils


def main():
    st.header("Text Classification")
    st.divider()
    st.subheader("Step 1: File uploader, make sure the two files have the same format")

    model_name = utils.sidebar()

    df_train = utils.upload_file("Train CSV file")
    df_test = utils.upload_file("Test CSV file")

    if df_train is None or df_test is None:
        st.stop()

    st.divider()
    st.subheader("Step 2: Pick up the text and label columns")
    options = utils.get_text_label(df_train)

    if not options:
        st.stop()

    text_col, label_col = options

    df_train[text_col] = df_train[text_col].apply(lambda x: utils.text_pre_processing(x))
    df_test[text_col] = df_test[text_col].apply(lambda x: utils.text_pre_processing(x))

    vectorizer = feature_extraction.text.TfidfVectorizer(max_features=10000, ngram_range=(1, 2))

    corpus = df_train[text_col]
    vectorizer.fit(corpus)

    X_train = vectorizer.transform(corpus)
    y_train = df_train[label_col]

    X_test = df_test[text_col].values
    y_test = df_test[label_col]


    st.divider()
    st.subheader("Step 3: Choose a model from left side bar")

    if not model_name:
        st.stop()

    classifier = naive_bayes.MultinomialNB() if model_name == 'Naive Bayes' else LogisticRegression(solver='liblinear')

    model = pipeline.Pipeline([("vectorizer", vectorizer), ("classifier", classifier)])
    model["classifier"].fit(X_train, y_train)
    predicted_test = model.predict(X_test)

    f1 = f1_score(y_test, predicted_test, average='weighted')

    st.write(f"The f1 score of {model_name} model is {f1:.2f}.")
    utils.draw(confusion_matrix(y_test, predicted_test))

    st.divider()
    st.subheader("Step 4: Download the predicted test result")

    df_test['predicted'] = predicted_test
    utils.download_file(df_test, model_name)


if __name__ == "__main__":
    main()
