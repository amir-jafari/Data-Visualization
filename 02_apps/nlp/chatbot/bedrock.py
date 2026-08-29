# %% ----- Imports
import sys
import boto3
from pathlib import Path
from botocore.exceptions import ClientError
import json

# %% ----- Configuration
# Credentials come from the one .env at the repo root, out of its [bedrock]
# block. The [s3] block right above it uses the very same field names but is a
# different account -- the tag is what keeps them apart.
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))
from env_config import ENV_FILE, section

_CREDS = section("bedrock")

AWS_ACCESS_KEY_ID = _CREDS.get("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = _CREDS.get("aws_secret_access_key")
AWS_SESSION_TOKEN = _CREDS.get("aws_session_token")
AWS_REGION = _CREDS.get("region", "us-east-1")
MODEL_ID = _CREDS.get("model_id", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")

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
