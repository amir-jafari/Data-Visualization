# s3 — where the data lives

No datasets, images, audio or video are stored in this repo. They live in

```
s3://dats-dl/ajafari@gwu.edu/streamlit/
    static/   flower.png, background.webp, myaudio.ogg, myvideo.mp4, gwu.jpg
    data/     the sample datasets, mirroring the 02_apps/ tree
```

and are fetched at runtime. Two files here:

- **`s3_utils.py`** — what the apps import. One place that talks to S3.
- **`s3_manager.py`** — a command-line tool to list, upload, download, delete.

## Setup

```bash
cp .env.example .env      # then paste your keys into .env at the repo root
```

One `.env` at the repo root serves everything — it is the only place the code
looks. It holds two credential sets from two different AWS accounts, using the
same field names and told apart by the `[tag]` above each block:

```ini
[s3]
region=us-east-1
aws_access_key_id=ASIA...
aws_secret_access_key=...
aws_session_token=...

[bedrock]
...
```

That's the same layout the AWS console gives you, so you can paste a block
straight in without renaming anything, and one set can't overwrite the other.
Filling in only `[s3]` is enough for everything here.

`.env` is git-ignored. Real environment variables and `~/.aws/credentials`
override it if you'd rather use those.

> A `.pem` file will not work — that's an SSH key, it can't sign S3 requests.
> On an EC2 instance you SSH into, the instance's IAM role is used and there is
> nothing to configure.

## When the keys expire

Learner Lab credentials are temporary. When they die, any app that reads from
S3 stops and shows a **"AWS keys need to be updated"** panel:

1. Restart your AWS lab and copy the fresh credentials.
2. Paste them into the **`[s3]`** block of the repo-root `.env` — the session
   token is **required** for keys starting `ASIA`. Leave `[bedrock]` alone;
   it's a different account.
3. Press the retry button in the app — no restart needed.

## Using it in your own code

```python
from s3 import s3_utils

df    = s3_utils.read_csv("data/time_series/forecasting/air_pollution.csv")
image = s3_utils.read_image("static/flower.png")
raw   = s3_utils.read_bytes("static/myvideo.mp4")

# a file picker that browses S3 by default, with upload as the fallback
file = s3_utils.file_input("CSV data file",
                           folder="data/data_mining/classification",
                           types=["csv"])
```

For that import to work from any sub-folder, apps put the repo root on the path
first:

```python
import sys
from pathlib import Path
REPO_ROOT = next(p for p in Path(__file__).resolve().parents if (p / "s3").is_dir())
sys.path.insert(0, str(REPO_ROOT))
```

## Command line

Every path is relative to `ajafari@gwu.edu/`, so you can't reach outside your
own prefix by accident.

```bash
python s3/s3_manager.py ls streamlit/ -r        # list, recursively
python s3/s3_manager.py upload model.pt         # -> ajafari@gwu.edu/model.pt
python s3/s3_manager.py upload ./results results/ -r
python s3/s3_manager.py download data/train.csv C:\tmp\
python s3/s3_manager.py rm old_model.pt         # asks first; -y to skip
```

Extra flags: `--profile NAME`, `--region`. Uploads and downloads use boto3's
multipart transfer with live progress, so large checkpoints are fine.
