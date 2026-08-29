"""
Reads the repo's single credentials file, `.env` at the repo root.

Two different AWS accounts live in there under the same field names, kept
apart by a `[tag]` above each block -- the format the AWS console gives you:

    [s3]
    region=us-east-1
    aws_access_key_id=ASIA...
    aws_secret_access_key=...
    aws_session_token=...

    [bedrock]
    region=us-east-1
    aws_access_key_id=ASIA...
    ...

Because every key belongs to the tag above it, pasting one block can never
overwrite the other -- which a flat KEY=VALUE file could, silently.

    from env_config import section
    creds = section("s3")        # {'region': ..., 'aws_access_key_id': ...}

Uses configparser from the standard library, so nothing extra to install.
"""

import configparser
from pathlib import Path

ENV_FILE = Path(__file__).resolve().parent / ".env"

# What each tag is for, used in the "you need to set this up" messages.
TAGS = {"s3": "S3 data access", "bedrock": "the Bedrock LLM"}


def section(tag, path=None):
    """
    Return one tagged block as a dict of lower-case keys.

    Missing file, missing tag, or blank values all come back as {} / absent
    rather than raising -- callers decide how loudly to complain.
    """
    path = Path(path) if path else ENV_FILE
    if not path.is_file():
        return {}

    parser = configparser.ConfigParser(interpolation=None)
    try:
        parser.read(path, encoding="utf-8")
    except configparser.MissingSectionHeaderError:
        raise SystemExit(
            f"\n{path} is in the old flat format (no [s3] / [bedrock] tags).\n"
            f"Copy .env.example over it and paste your keys under the tags.\n"
        )
    except configparser.Error as exc:
        raise SystemExit(f"\nCould not read {path}: {exc}\n")

    if not parser.has_section(tag):
        return {}

    return {key: value.strip().strip("'\"")
            for key, value in parser.items(tag)
            if value and value.strip()}


# Field name in the file -> the environment variable boto3 actually looks for.
BOTO_ENV = {
    "aws_access_key_id": "AWS_ACCESS_KEY_ID",
    "aws_secret_access_key": "AWS_SECRET_ACCESS_KEY",
    "aws_session_token": "AWS_SESSION_TOKEN",
    "region": "AWS_DEFAULT_REGION",
}


def as_boto_env(tag, path=None):
    """One tagged block, re-keyed to the AWS_* names boto3 reads."""
    creds = section(tag, path)
    return {env: creds[field] for field, env in BOTO_ENV.items() if field in creds}
