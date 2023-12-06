import io
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

import warnings
warnings.filterwarnings("ignore")

import utils


def main():
    # Save the state of clicking button for the step 2
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False

    options_dic = {
        "Decision Tree": 1,
        "Random Forest": 2,
        "Support Vector Machine": 3,
        "KNN": 4,
        "Naive Bayes": 5,
        "Logistic Regression": 6,
    }
    model_name = utils.sidebar(options_dic.keys())

    st.header("Classification")
    st.divider()
    st.subheader("Step 1: File uploader")

    data = utils.upload_file("CSV data file")

    if data is None:
        st.stop()

    st.divider()
    st.subheader("Step 2: Data preprocessing")

    y_column = st.selectbox(
        'Select the y label column',
        data.columns,
    )

    dropped_columns = st.multiselect(
        'Drop the unnnecessary columns',
        [col for col in data.columns if col != y_column],
        []
    )

    if st.button('Confirm choosing', type="primary"):
        st.session_state.button_clicked = True

    if st.session_state.button_clicked is False:
        st.stop()

    data.drop(dropped_columns, axis=1, inplace=True)

    st.write("Display the count of null values for columns with more than 0 nulls.")
    null_counts = data.isnull().sum()
    st.write(null_counts[null_counts > 0])

    if st.toggle('Drop rows with NA values (needed for all models except Decision Tree)'):
        data = data.dropna(axis=0)

    encoding_columns = st.multiselect(
        'Choose the columns that need encoding',
        [col for col in data.columns if (col != y_column and col not in dropped_columns)],
        []
    )

    # encoding the class with sklearn's LabelEncoder
    class_le = LabelEncoder()

    for col in encoding_columns:
        data[col] = class_le.fit_transform(data[col])

    st.write(f'The y column of the dataframe is {y_column}, and the modified dataframe looks as follow:')
    st.write(data.head())

    y = data[y_column].values
    X = data.drop(y_column, axis=1).values

    # fit and transform the class
    y = class_le.fit_transform(y)

    # split the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    st.divider()
    st.subheader("Step 3: EDA")

    tab1, tab2 = st.tabs(["data.describe()", "data.info()"])
    with tab1:
        st.write('***data.describe():***', data.describe())

    with tab2:
        st.write('***data.info():***')
        buffer = io.StringIO()
        data.info(buf=buffer)
        st.text(buffer.getvalue())

    st.write("***Plot for each column***")
    columns = data.columns.tolist()
    tabs = st.tabs(columns)

    for i in range(len(columns)):
        with tabs[i]:
            plot_column = columns[i]

            col1, col2 = st.columns(2)

            with col1:
                # Boxplot for a numerical column
                plt.figure()
                sns.boxplot(x=data[plot_column])
                plt.title('Boxplot of numerical_column')
                st.pyplot(plt)

                # # Histogram for a numerical column
                # plt.figure(figsize=(8, 6))
                # sns.histplot(data[plot_column], kde=True)
                # plt.title('Distribution of numerical_column')
                # plt.xlabel('Value')
                # plt.ylabel('Frequency')
                # st.pyplot(plt)

            with col2:
                # Bar chart for a categorical column
                plt.figure()
                sns.countplot(x=data[plot_column])
                plt.title('Count of categorical_column')
                plt.xlabel('Category')
                plt.ylabel('Count')
                st.pyplot(plt)


    st.divider()
    st.subheader("Step 4: Choose model and set up parameters")
    if not model_name:
        st.warning("***Pick up the model from the left side bar***")
        st.stop()

    index = options_dic[model_name]

    st.write(f"The model you choose is ***{model_name}***")

    if index == 1:
        clf = utils.decision_tree_predict(X_train, y_train)
    elif index == 2:
        columns = data.drop(y_column, axis=1).columns
        clf, X_test = utils.random_forest_predict(X_train, y_train, X_test, columns)
    elif index == 3:
        clf = utils.SVM_predict(X_train, y_train)
    elif index == 4:
        clf = utils.KNN_predict(X_train, y_train)
    elif index == 5:
        clf = utils.NB_predict(X_train, y_train)
    elif index == 6:
        clf = utils.Logistic_predict(X_train, y_train)
    else:
        st.error("The index does not exist")
        st.stop()

    st.divider()
    st.subheader("Step 5: Get the result")

    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred) * 100
    st.write(f"The accuracy of {index}. {model_name} model is : {accuracy:.2f} %")

    st.text('Classification Report:\n' + classification_report(y_test, y_pred))

    conf_matrix = confusion_matrix(y_test, y_pred)

    # st.write(type(conf_matrix))
    class_names = data[y_column].unique()
    df_cm = pd.DataFrame(conf_matrix, index=class_names, columns=class_names)

    utils.draw(df_cm)


if __name__ == "__main__":
    main()
