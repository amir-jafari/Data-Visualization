import streamlit as st

from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import torch
import librosa

import utils

# --- make the repo's s3/ helpers importable, wherever you run this from ------
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
from s3 import s3_utils

# All data for this app lives in S3, never on disk:
#   s3://dats-dl/ajafari@gwu.edu/streamlit/data/Audio/
S3_FOLDER = "data/Audio"



def main():
    st.header("Audio Transcription")
    st.divider()
    st.subheader("Step 1: Audio File Upload and Play")
    model_name = utils.sidebar()

    # Defaults to browsing S3; "Upload from my computer" is the fallback.
    uploaded_file = s3_utils.file_input("audio file", folder=S3_FOLDER,
                                        types=['mp3', 'wav', 'ogg', 'flac'])

    if uploaded_file is not None:
        # wav2vec2-base-960h was trained on 16kHz audio -- resample here so the
        # model gets the sample rate it expects instead of librosa's 22050Hz default.
        y, sr = librosa.load(uploaded_file, sr=16000)

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
        input_values = st.session_state['processor'](y, sampling_rate=sr, return_tensors="pt", padding="longest").input_values  # Batch size 1

        # retrieve logits
        logits = st.session_state['model'](input_values).logits

        # take argmax and decode
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = st.session_state['processor'].batch_decode(predicted_ids)

        st.write("***The transcription is as follows***")
        st.write(transcription[0])


if __name__ == "__main__":
    main()
