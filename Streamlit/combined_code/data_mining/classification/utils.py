import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression

import warnings
warnings.filterwarnings("ignore")


def sidebar(options):
    with st.sidebar:
        genre = st.radio(
            "Choose your model",
            options,
            index=None,
        )
        return genre


def upload_file(file_name):
    file = st.file_uploader(f"Choose the {file_name}", type="csv")
    no_header = st.checkbox("Check it if the dataset doesn't have the header row", value=False)

    if file is not None:
        if no_header:
            df = pd.read_csv(file, header=None)
            df.columns = [f'Column{index}' for index in df.columns]
        else:
            df = pd.read_csv(file)

        st.write(df.head())
        return df


def decision_tree_predict(X_train, y_train):
    criterion = st.radio(
        "Choose your criterion",
        ['gini', 'entropy'],
    )
    max_depth = st.number_input("Type the max_depth", value=3, min_value=1, max_value=20, step=1,
                                placeholder="Type a int number...")
    min_samples_leaf = st.number_input("Type the min_samples_leaf", value=5, min_value=0, max_value=20,
                                       placeholder="Type a number...")

    if not max_depth or not min_samples_leaf:
        st.stop()

    clf = DecisionTreeClassifier(criterion=criterion, random_state=100, max_depth=max_depth,
                                 min_samples_leaf=min_samples_leaf)
    clf.fit(X_train, y_train)
    return clf


def random_forest_predict(X_train, y_train, X_test, columns):
    n_estimators = st.number_input("Type the n_estimators", value=100, min_value=1, max_value=10000, step=1,
                                   placeholder="Type a int number...")
    if not n_estimators:
        st.stop()

    clf = RandomForestClassifier(n_estimators=n_estimators, random_state=100)
    clf.fit(X_train, y_train)

    importances = clf.feature_importances_
    # convert the importances into one-dimensional 1darray with corresponding df column names as axis labels
    f_importances = pd.Series(importances, columns)

    # sort the array in descending order of the importances
    f_importances.sort_values(ascending=False, inplace=True)

    st.write('Plot feature importances in descending order')
    f_importances.plot(x='Features', y='Importance', kind='bar')
    st.pyplot(plt)

    if st.toggle('Use K features to do predict'):
        f_importances_lst = f_importances.index.tolist()

        end_feature = st.select_slider(
            'Select a range of features to use to predict',
            options=f_importances_lst,
            value=(f_importances_lst[-1]))
        st.write('You selected features between', f_importances_lst[0], 'and', end_feature)

        end_index = f_importances_lst.index(end_feature) + 1

        # select the training dataset on k-features
        newX_train = X_train[:, clf.feature_importances_.argsort()[::-1][:end_index]]

        # select the testing dataset on k-features
        newX_test = X_test[:, clf.feature_importances_.argsort()[::-1][:end_index]]

        clf_k_features = RandomForestClassifier(n_estimators=n_estimators, random_state=100)
        clf_k_features.fit(newX_train, y_train)

        return clf_k_features, newX_test

    return clf, X_test


def SVM_predict(X_train, y_train):
    kernel = st.radio(
        "Choose your kernel",
        ['linear', 'rbf'],
    )
    C_value = st.number_input("Type the C value", value=1.0, min_value=0.0, max_value=100.0, step=0.1,
                              placeholder="Type a number...")

    if kernel == 'linear':
        svm = SVC(kernel='linear', C=C_value, random_state=0)
    else:
        gamma = st.number_input("Type the gamma value", value=0.2, min_value=0.0, max_value=100.0, step=0.1,
                                placeholder="Type a number...")

        svm = SVC(kernel='rbf', random_state=0, gamma=gamma, C=C_value)

    svm.fit(X_train, y_train)

    return svm


def KNN_predict(X_train, y_train):
    metric = st.radio(
        "Choose your metric",
        ['minkowski'],
    )
    n_neighbors = st.number_input("Type the n_neighbors", value=1, min_value=1, max_value=10000, step=1,
                                  placeholder="Type a int number...")
    p_value = st.number_input("Type the p value", value=2, min_value=1, max_value=10000, step=1,
                              placeholder="Type a int number...")

    knn = KNeighborsClassifier(n_neighbors=n_neighbors, p=p_value, metric=metric)
    knn.fit(X_train, y_train)
    return knn


def NB_predict(X_train, y_train):
    clf = GaussianNB()
    clf.fit(X_train, y_train)
    return clf


def Logistic_predict(X_train, y_train):
    C_value = st.number_input("Type the C value", value=1000.0, min_value=1.0, max_value=100000.0, step=0.1,
                              placeholder="Type a number...")

    lr = LogisticRegression(C=C_value, random_state=0)
    lr.fit(X_train, y_train)
    return lr


def draw(cm):
    sns.heatmap(cm, annot=True)
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    st.pyplot(plt)
