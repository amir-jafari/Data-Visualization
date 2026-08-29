# %% ----- Imports
import os
import boto3
from pathlib import Path
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv

# %% ----- Configuration
# One .env for the whole repo, at its root. Pinned explicitly rather than
# relying on dotenv's upward directory search, which could pick up an
# unrelated .env elsewhere on the machine.
#
# The Bedrock credentials are the BEDROCK_AWS_* ones; the plain AWS_* keys in
# the same file belong to S3 and are a different account.
ENV_PATH = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=ENV_PATH)



def env(name, default=None):
    """Look up a .env value in either case -- the file is written lower case."""
    return os.getenv(name.lower()) or os.getenv(name.upper()) or default


AWS_ACCESS_KEY_ID = env("bedrock_aws_access_key_id")
AWS_SECRET_ACCESS_KEY = env("bedrock_aws_secret_access_key")
AWS_SESSION_TOKEN = env("bedrock_aws_session_token")
AWS_REGION = env("bedrock_aws_region", "us-east-1")
MODEL_ID = env("bedrock_model_id", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")

# %% ----- LLM API Invocation
def invoke_llm_api(prompt, conversation_history=None, max_tokens=1000, temperature=0, top_k=250):
    try:
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            aws_session_token=AWS_SESSION_TOKEN
        )

        bedrock_client = session.client("bedrock-runtime", region_name=AWS_REGION)

        messages = []
        system_message = None

        if conversation_history:
            for message in conversation_history:
                if message["role"] == "system":
                    system_message = message["content"]
                else:
                    messages.append(message)

        messages.append({
            "role": "user",
            "content": prompt
        })

        body_content = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_k": top_k,
            "messages": messages
        }

        if system_message:
            body_content["system"] = system_message

        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body_content)
        )
        response_body = response['body'].read().decode()

        return response_body.strip()

    except ClientError:
        return None
    except Exception:
        return None
