import re
import streamlit as st
import pandas as pd
import nltk
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

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
    no_header = st.checkbox("Check it if the dataset doesn't have the header row")

    if file is not None:
        if no_header:
            df = pd.read_csv(file, header=None)
            df.columns = [f'Column{index}' for index in df.columns]
        else:
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


def desicion_tree_predict(X_train, y_train, X_test, criterion):
    # perform training with giniIndex.
    # creating the classifier object
    clf = DecisionTreeClassifier(criterion=criterion, random_state=100, max_depth=3, min_samples_leaf=5)

    # performing training
    clf.fit(X_train, y_train)

    # predicton on test using gini
    y_pred = clf.predict(X_test)
    return y_pred

def random_forest_predict(X_train, y_train, X_test, columns, k_features=None):
    # specify random forest classifier
    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)

    # get feature importances
    importances = clf.feature_importances_

    # convert the importances into one-dimensional 1darray with corresponding df column names as axis labels
    f_importances = pd.Series(importances, columns)

    # sort the array in descending order of the importances
    f_importances.sort_values(ascending=False, inplace=True)

    # make the bar Plot from f_importances
    f_importances.plot(x='Features', y='Importance', kind='bar', figsize=(16, 9), rot=90, fontsize=15)

    # show the plot
    plt.tight_layout()
    st.pyplot(plt)

    if k_features:
        # select features to perform training with random forest with k columns
        # select the training dataset on k-features
        newX_train = X_train[:, clf.feature_importances_.argsort()[::-1][:15]]

        # select the testing dataset on k-features
        newX_test = X_test[:, clf.feature_importances_.argsort()[::-1][:15]]

        # specify random forest classifier
        clf_k_features = RandomForestClassifier(n_estimators=100)

        # train the model
        clf_k_features.fit(newX_train, y_train)

        # prediction on test using k features
        y_pred = clf_k_features.predict(newX_test)
        y_pred_score = clf_k_features.predict_proba(newX_test)
    else:
        # predicton on test using all features
        y_pred = clf.predict(X_test)
        y_pred_score = clf.predict_proba(X_test)

    # # st.write(f"y_pred_score is {y_pred_score}")
    # print("ROC_AUC : ", roc_auc_score(y_test, y_pred_score[:, 1]) * 100)

    return y_pred


def SVM_predict(X_train, y_train, X_test, linear=True):
    sc = StandardScaler()
    sc.fit(X_train)
    X_train_std = sc.transform(X_train)
    X_test_std = sc.transform(X_test)

    if linear:
        svm = SVC(kernel='linear', C=1.0, random_state=0)
    else:
        svm = SVC(kernel='rbf', random_state=0, gamma=0.2, C=1.0)

    svm.fit(X_train, y_train)

    y_pred = svm.predict(X_test)
    return y_pred


def sidebar(options):
    with st.sidebar:
        genre = st.radio(
            "Choose your model",
            options,
            # captions=["Use Naive Bayes to predict.", "Use logistic regression to predict."],
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
