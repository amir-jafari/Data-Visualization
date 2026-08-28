import streamlit as st
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer

stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def get_txt():
    txt = st.text_area(
        "Text to clean",
        "Check out the latest tech news at https://example.com! Meet me @TechConference2023 to discuss the future of AI. There are over 10,000 participants expected. Isn't that amazing? However, we should be aware that not all trends are beneficial. @JaneDoe might disagree, but I believe that thorough analysis is crucial. Remember to RSVP by 5pm!",
    )

    st.write(f'You wrote {len(txt)} characters.')
    return txt


def clean(text, index):
    if index == 0:
        # Remove URLs
        text = re.sub(r'http\S+', '', text)
    elif index == 1:
        # Remove mentions
        text = re.sub(r'@[A-Za-z0-9]+', '', text)
    elif index == 2:
        # Remove numbers
        text = re.sub(r'\d+', '', text)
    elif index == 3:
        # Remove punctuation
        text = re.sub(r'[^a-zA-Z]', ' ', text)
    elif index == 4:
        # Convert to lowercase
        text = text.lower()
    elif index >= 5:
        # Tokenize
        words = text.split()
        if index == 5:
            # Remove stop words
            words = [word for word in words if word not in stop_words]
        elif index == 6:
            # Stem words
            words = [stemmer.stem(word) for word in words]
        elif index == 7:
            # Lemmatize words
            words = [lemmatizer.lemmatize(word) for word in words]
        # Join words back into a string
        text = ' '.join(words)
    return text


def sidebar():
    with st.sidebar:
        st.write("Which text cleaning methods will you want to use?")
        # Define a list of options
        options = [
            (0, "Remove URLs"),
            (1, "Remove mentions"),
            (2, "Remove numbers"),
            (3, "Remove punctuation",),
            (4, "Convert to lowercase"),
            (5, "Remove stop words"),
            (6, "Stem words",),
            (7, "Lemmatize words"),
        ]

        # Create a dictionary to hold the selection status of each option
        selected_options = {}

        for option in options:
            # Use st.checkbox for each option
            selected = st.checkbox(option[1], key=option[0], value=True)
            selected_options[option] = selected

        # print('selected_options', selected_options)
        # Filter the selected options
        selected = [option for option, selected in selected_options.items() if selected]

        return selected
