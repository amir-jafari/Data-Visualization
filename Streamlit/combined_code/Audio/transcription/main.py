import streamlit as st

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa

import utils


def main():
    st.header("Audio Transcription")
    st.divider()
    st.subheader("Step 1: Audio File Upload and Play")
    model_name = utils.sidebar()

    uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'ogg', 'flac'])

    if uploaded_file is not None:
        y, sr = librosa.load(uploaded_file)
        print('len(y), sr', len(y), sr)

        st.audio(y, format='audio/ogg', sample_rate=sr)

        st.divider()
        st.subheader("Step 2: Choose a model from left side bar")

        if not model_name:
            st.stop()

        st.write(f'The model you are using is **{model_name}**')

        st.divider()
        st.subheader("Step 3: Get the transcription of the audio")

        # load model and tokenizer
        if 'processor' not in st.session_state:
            st.session_state['processor'] = Wav2Vec2Processor.from_pretrained(model_name)
        if 'model' not in st.session_state:
            st.session_state['model'] = Wav2Vec2ForCTC.from_pretrained(model_name)

        # tokenize
        input_values = st.session_state['processor'](y, return_tensors="pt", padding="longest").input_values  # Batch size 1

        # retrieve logits
        logits = st.session_state['model'](input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = st.session_state['processor'].batch_decode(predicted_ids)

        st.write("***The transcription is as follows***")
        st.write(transcription[0])


if __name__ == "__main__":
    main()
