import time

import streamlit as st

from sklearn import feature_extraction,  naive_bayes, pipeline
from sklearn.metrics import classification_report, confusion_matrix, f1_score
from sklearn.linear_model import LogisticRegression


from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import utils


def main():
    st.header("Classification")
    st.divider()
    st.subheader("Step 1: File uploader")

    options_dic = {
        "Decision Tree (gini)": 0,
        "Decision Tree (entropy)": 1,
        "Random Forest": 2,
        "Support Vector Machine": 3,
        "KNN": 4,
        "Naive Bayes": 5,
        "Logistic Regression": 6,
    }
    model_name = utils.sidebar(options_dic.keys())

    data = utils.upload_file("CSV data file")

    if data is None:
        st.stop()

    st.divider()
    st.subheader("Step 2: Pick up the model from the left side bar")

    if not model_name:
        st.stop()

    index = options_dic[model_name]

    st.write(f"The model you choose is {model_name}")

    st.divider()
    st.subheader("Step 3: Data preprocessing")

    y_column = st.selectbox(
        'Select the y column',
        data.columns,
    )

    dropped_columns = st.multiselect(
        'Drop the unnnecessary columns',
        data.columns,
        []
    )

    if y_column in dropped_columns:
        st.error("You can not drop the y column")
        st.stop()

    if not st.button('Confirm choosing', type="primary"):
        st.stop()

    data.drop(dropped_columns, axis=1, inplace=True)

    st.write(f'The y column of the dataframe is {y_column}, and the modified dataframe looks as follow:')
    st.write(data.head())

    y = data[y_column].values
    X = data.drop(y_column, axis=1).values

    # encloding the class with sklearn's LabelEncoder
    class_le = LabelEncoder()

    # fit and transform the class
    y = class_le.fit_transform(y)

    # split the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    st.divider()
    st.subheader("Step 4: Get the result")

    if index == 0:
        y_pred = utils.desicion_tree_predict(X_train, y_train, X_test, "gini")
    elif index == 1:
        y_pred = utils.desicion_tree_predict(X_train, y_train, X_test, "entropy")
    elif index == 2:
        columns = data.drop(y_column, axis=1).columns
        y_pred = utils.random_forest_predict(X_train, y_train, X_test, columns)
    elif index == 3:
        y_pred = utils.SVM_predict(X_train, y_train, X_test, linear=True)
    elif index == 4:
        from sklearn.neighbors import KNeighborsClassifier
        knn = KNeighborsClassifier(n_neighbors=1, p=2, metric='minkowski')
        knn.fit(X_train, y_train)
        y_pred = knn.predict(X_test)
    elif index == 5:
        clf = GaussianNB()
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
    elif index == 6:
        lr = LogisticRegression(C=1000.0, random_state=0)
        lr.fit(X_train, y_train)
        y_pred = lr.predict(X_test)
    else:
        st.error("The index does not exist")
        st.stop()

    class_names = data[y_column].unique()

    accuracy = accuracy_score(y_test, y_pred) * 100
    st.write(f"The accuracy of {index}. {model_name} model is : {accuracy:.2f} %")

    # st.write("**Classification Report:**")
    st.text('Classification Report:\n' + classification_report(y_test, y_pred))

    conf_matrix = confusion_matrix(y_test, y_pred)

    st.write('The class_names are', ', '.join(class_names))

    df_cm = pd.DataFrame(conf_matrix, index=class_names, columns=class_names)

    # plt.figure(figsize=(5, 5))
    # hm = sns.heatmap(df_cm, cbar=False, annot=True, square=True, fmt='d', annot_kws={'size': 20},
    #                  yticklabels=df_cm.columns, xticklabels=df_cm.columns)
    # hm.yaxis.set_ticklabels(hm.yaxis.get_ticklabels(), rotation=0, ha='right', fontsize=20)
    # hm.xaxis.set_ticklabels(hm.xaxis.get_ticklabels(), rotation=0, ha='right', fontsize=20)
    # plt.ylabel('True label', fontsize=20)
    # plt.xlabel('Predicted label', fontsize=20)
    # plt.tight_layout()
    # st.pyplot(plt)

    utils.draw(conf_matrix)


if __name__ == "__main__":
    main()
