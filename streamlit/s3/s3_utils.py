"""
Shared S3 access for every Streamlit app in this repo.

All data for these apps lives in S3, not on disk:

    s3://dats-dl/ajafari@gwu.edu/streamlit/
        static/       flower.png, background.webp, myaudio.ogg, myvideo.mp4, gwu.jpg
        data/         the sample datasets, mirroring the apps/ tree
        CheatSheet/   streamlit_cheat_sheet.pdf

Credentials are read from the [s3] block of the repo-root .env (the same file
s3_manager.py uses), so when the Learner Lab keys expire you only update that
one file. The [bedrock] block beside it uses the same field names but is the
chatbot's LLM account, and is untouched here. Real environment variables and
~/.aws/credentials still win if they are set.

Typical use inside an app:

    from s3 import s3_utils
    data = s3_utils.read_csv("data/time_series/forecasting/air_pollution.csv")

    # a file picker that browses S3 by default, with upload as the fallback
    file = s3_utils.file_input("CSV data file", folder="data/data_mining/classification")
"""

import io
import os
import sys
from pathlib import Path

import boto3
import streamlit as st
from boto3.exceptions import Boto3Error
from botocore.exceptions import BotoCoreError, ClientError, NoCredentialsError

BUCKET = "dats-dl"
PREFIX = "ajafari@gwu.edu/streamlit/"
REGION = "us-east-1"

CRED_KEYS = (
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "AWS_SESSION_TOKEN",
    "AWS_DEFAULT_REGION",
)

# Credentials come from the [s3] block of the one .env at the repo root. The
# [bedrock] block beside it uses identical field names but belongs to the
# chatbot's LLM -- the tag is what keeps the two accounts apart.
REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))
from env_config import ENV_FILE, as_boto_env

# Whatever was already in the real environment when this module was imported
# takes precedence over the .env file, so `export AWS_...` still works.
_REAL_ENV = {k: os.environ.get(k) for k in CRED_KEYS}


# --------------------------------------------------------------------------- #
# credentials
# --------------------------------------------------------------------------- #
def env_file():
    """The .env we are actually using, or None if there isn't one."""
    return ENV_FILE if ENV_FILE.is_file() else None


def load_credentials():
    """
    Push the [s3] block into os.environ and return a fingerprint.

    Re-read every run rather than cached, so pasting fresh keys into .env and
    hitting "Rerun" is enough to pick them up -- no restart required.
    """
    file_values = as_boto_env("s3")

    for key in CRED_KEYS:
        real = _REAL_ENV.get(key)
        value = real or file_values.get(key)
        if value:
            os.environ[key] = value
        else:
            os.environ.pop(key, None)

    # Enough to tell one credential set from another without holding the secret.
    return "|".join(str(len(os.environ.get(k, ""))) + os.environ.get(k, "")[:6]
                    for k in CRED_KEYS)


@st.cache_resource(show_spinner=False)
def _build_client(fingerprint):
    # fingerprint is unused inside, but it is what invalidates this cache when
    # the keys in .env change.
    return boto3.Session().client("s3", region_name=os.environ.get("AWS_DEFAULT_REGION") or REGION)


def get_client():
    return _build_client(load_credentials())


# --------------------------------------------------------------------------- #
# error handling -- the "your keys expired" message
# --------------------------------------------------------------------------- #
CREDENTIAL_CODES = {
    "ExpiredToken", "ExpiredTokenException", "InvalidAccessKeyId",
    "SignatureDoesNotMatch", "AccessDenied", "InvalidClientTokenId",
    "UnrecognizedClientException", "AuthFailure", "RequestExpired",
    "TokenRefreshRequired", "InvalidToken",
}

_HINTS = {
    "ExpiredToken": "Your temporary AWS credentials have expired.",
    "ExpiredTokenException": "Your temporary AWS credentials have expired.",
    "RequestExpired": "Your temporary AWS credentials have expired.",
    "InvalidAccessKeyId": "The access key is not valid, or a session token is missing. "
                          "Keys starting with ASIA are temporary and also need AWS_SESSION_TOKEN.",
    "SignatureDoesNotMatch": "The secret key does not match the access key -- check for a "
                             "truncated paste or stray whitespace.",
    "AccessDenied": "These credentials are not allowed to read this bucket.",
    "InvalidToken": "The session token is not valid any more.",
    "NoSuchBucket": f"Bucket '{BUCKET}' was not found in this region.",
    "NoSuchKey": "That object does not exist in S3 yet.",
    "404": "That object does not exist in S3 yet.",
}


def error_code(exc):
    if isinstance(exc, NoCredentialsError):
        return "NoCredentials"
    if isinstance(exc, ClientError):
        return exc.response.get("Error", {}).get("Code", "Unknown")
    message = str(exc)
    for code in CREDENTIAL_CODES | {"NoSuchBucket", "NoSuchKey"}:
        if code in message:
            return code
    return "Unknown"


def is_credential_problem(exc):
    return error_code(exc) in CREDENTIAL_CODES | {"NoCredentials"}


def show_error(exc, key=None):
    """Render a readable failure box. Credential problems get the loud version."""
    code = error_code(exc)
    location = str(ENV_FILE)

    if is_credential_problem(exc):
        st.error(
            f"### :key: AWS keys need to be updated\n\n"
            f"This app reads its data from `s3://{BUCKET}/{PREFIX}`, and S3 just "
            f"rejected the current credentials (`{code}`).\n\n"
            f"**{_HINTS.get(code, 'The credentials are not being accepted.')}**\n\n"
            f"**To fix it:**\n"
            f"1. Start your AWS lab again and copy the fresh credentials.\n"
            f"2. Paste them into the **`[s3]`** block of `{location}`:\n"
            f"   `aws_access_key_id`, `aws_secret_access_key`, and "
            f"`aws_session_token` (required for keys that start with `ASIA`).\n"
            f"   Leave the `[bedrock]` block below it alone -- it is a "
            f"different account.\n"
            f"3. Come back here and press the button below.\n"
        )
        if st.button(":arrows_counterclockwise: I updated the keys -- retry",
                     key=f"s3_retry_{key or code}"):
            st.cache_resource.clear()
            st.cache_data.clear()
            st.rerun()
    else:
        st.error(
            f"### Could not read from S3\n\n"
            f"`{code}` while reading "
            f"`s3://{BUCKET}/{PREFIX}{key or ''}`\n\n"
            f"{_HINTS.get(code, str(exc))}"
        )


def guard(exc, key=None):
    """Show the failure and halt the app -- there is nothing left to render."""
    show_error(exc, key)
    st.stop()


# --------------------------------------------------------------------------- #
# reading objects
# --------------------------------------------------------------------------- #
def full_key(rel_key):
    return PREFIX + str(rel_key).replace("\\", "/").lstrip("/")


def uri(rel_key):
    return f"s3://{BUCKET}/{full_key(rel_key)}"


@st.cache_data(show_spinner="Loading from S3...")
def _fetch(rel_key, _fingerprint):
    client = get_client()
    return client.get_object(Bucket=BUCKET, Key=full_key(rel_key))["Body"].read()


def read_bytes(rel_key, stop_on_error=True):
    """Download an object from your S3 streamlit/ folder and return its bytes."""
    try:
        return _fetch(rel_key, load_credentials())
    except (ClientError, BotoCoreError, Boto3Error, NoCredentialsError) as exc:
        if stop_on_error:
            guard(exc, rel_key)
        raise


def open_file(rel_key, stop_on_error=True):
    """Same as read_bytes, wrapped in a file-like object with a .name."""
    buffer = io.BytesIO(read_bytes(rel_key, stop_on_error))
    buffer.name = Path(rel_key).name
    return buffer


def read_csv(rel_key, stop_on_error=True, **kwargs):
    import pandas as pd
    return pd.read_csv(open_file(rel_key, stop_on_error), **kwargs)


def read_image(rel_key, stop_on_error=True):
    from PIL import Image
    return Image.open(open_file(rel_key, stop_on_error))


@st.cache_data(show_spinner=False)
def _list(folder, _fingerprint):
    client = get_client()
    prefix = full_key(folder)
    if prefix and not prefix.endswith("/"):
        prefix += "/"

    keys = []
    for page in client.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix=prefix):
        for obj in page.get("Contents", []):
            if not obj["Key"].endswith("/"):
                keys.append(obj["Key"][len(PREFIX):])
    return sorted(keys)


def list_files(folder="", types=None, stop_on_error=True):
    """List objects under a folder of your streamlit/ prefix, newest API call cached."""
    try:
        keys = _list(folder, load_credentials())
    except (ClientError, BotoCoreError, Boto3Error, NoCredentialsError) as exc:
        if stop_on_error:
            guard(exc, folder)
        raise

    if types:
        wanted = tuple("." + t.lower().lstrip(".") for t in types)
        keys = [k for k in keys if k.lower().endswith(wanted)]
    return keys


# --------------------------------------------------------------------------- #
# widgets
# --------------------------------------------------------------------------- #
def file_input(label, folder="data", types=None, key=None, container=None, prefer=None):
    """
    A file picker that browses S3 first.

    Returns a file-like object -- so it drops straight into pd.read_csv(),
    Image.open(), librosa.load() -- or None if nothing is selected yet.

    prefer: preselect the first file whose name contains this string, e.g.
            prefer="Train" so a Train picker doesn't default to Test.csv.
    """
    ui = container or st
    key = key or f"{folder}:{label}"

    source = ui.radio(
        label,
        ["Browse S3", "Upload from my computer"],
        index=0,
        horizontal=True,
        key=f"src_{key}",
        help=f"Files live in {uri(folder)}",
    )

    if source == "Upload from my computer":
        return ui.file_uploader(f"Choose the {label}", type=types, key=f"up_{key}")

    keys = list_files(folder, types)
    if not keys:
        ui.warning(f"No matching files found in {uri(folder)}")
        return None

    index = 0
    if prefer:
        index = next((i for i, k in enumerate(keys)
                      if prefer.lower() in Path(k).name.lower()), 0)

    choice = ui.selectbox(
        f"Choose the {label} from S3",
        keys,
        index=index,
        format_func=lambda k: Path(k).name,
        key=f"s3_{key}",
    )
    ui.caption(f":white_check_mark: {uri(choice)}")
    return open_file(choice)


def status_badge(container=None):
    """A small connection indicator, handy in a sidebar."""
    ui = container or st.sidebar
    try:
        get_client().head_bucket(Bucket=BUCKET)
        ui.caption(f":white_check_mark: S3 connected -- `{BUCKET}/{PREFIX}`")
        return True
    except (ClientError, BotoCoreError, Boto3Error, NoCredentialsError) as exc:
        ui.caption(f":x: S3 unavailable (`{error_code(exc)}`) -- keys may need updating")
        return False
