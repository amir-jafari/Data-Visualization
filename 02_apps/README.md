# 02_apps — the pieces put together

Real apps built from the widgets in `01_basics/`. Each folder is a `main.py`
(the page) plus a `utils.py` (the work), so you can read the UI and the logic
separately.

```bash
pip install -r requirements.txt -r requirements-apps.txt   # from the repo root
streamlit run 02_apps/data_mining/classification/main.py
```

| App | What it does | Extra setup |
| --- | --- | --- |
| `data_mining/classification` | Upload a CSV, pick a target, train 6 classifiers, compare | S3 keys |
| `data_mining/linear_regression` | OLS with statsmodels, diagnostics and plots | S3 keys |
| `time_series/forecasting` | Decomposition, models, error metrics | S3 keys |
| `nlp/text_cleaning` | Tokenize, stem, lemmatize, stop-word removal | — |
| `nlp/sentiment_analysis` | TextBlob polarity and subjectivity | — |
| `nlp/text_classification` | Train and evaluate a text classifier | S3 keys |
| `nlp/hate_speech_detector` | A HuggingFace moderation pipeline | downloads a model |
| `nlp/chatbot/*` | Five chatbots, simplest first — see below | varies |
| `vision/image_classification` | Classify an uploaded image | downloads a model |
| `vision/object_detection` | YOLO boxes on an image | downloads a model |
| `vision/image_caption` | Caption an image | downloads a model |
| `vision/background_remover` | Cut the background out of a photo | downloads a model |
| `vision/data_augmentation` | Albumentations transforms, applied live | S3 keys |
| `audio/audio_processing` | Waveform, spectrogram, filters with librosa | S3 keys |
| `audio/transcription` | Speech to text | downloads a model |

## The chatbots, in the order to read them

1. **`chat_echo`** — the chat loop and nothing else. ~30 lines.
2. **`dummy_chat_bot`** — adds streaming and canned replies.
3. **`open_source_chatbot`** — a local HuggingFace model via LangChain.
4. **`api_chatbot`** — a real LLM through AWS Bedrock.
5. **`agent_tools`** — the same, with tool calling.

The last two need Bedrock credentials. They live in the same repo-root `.env`
as the S3 keys — same field names, but under the `[bedrock]` tag, because it's
a separate AWS account:

```bash
cp .env.example .env      # then fill in the [bedrock] block
```

Keep both tags in the file. A key belongs to the tag above it, so the two
accounts can't overwrite each other.

Both read that one file through the shared `chatbot/bedrock.py`.

## Where the data comes from

Nothing is stored in this repo. Apps marked *S3 keys* call
`s3_utils.file_input(...)`, which gives you a picker that browses the course S3
bucket by default and falls back to uploading your own file. Fill in the
`[s3]` block of the repo-root `.env` first — see
[`../s3/README.md`](../s3/README.md).

*Downloads a model* means the first run pulls weights from HuggingFace and is
slow; after that they're cached locally.
