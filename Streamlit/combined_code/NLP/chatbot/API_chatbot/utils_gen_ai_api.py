# %% ----- Imports
import os
import boto3
from pathlib import Path
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv

# %% ----- Configuration
# One shared .env for every chatbot app, kept in the parent `chatbot/` dir.
# Pinned explicitly rather than relying on dotenv's upward directory search,
# which could pick up an unrelated .env elsewhere in the repo tree.
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

AWS_ACCESS_KEY_ID = os.getenv("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.getenv("aws_secret_access_key")
AWS_SESSION_TOKEN = os.getenv("aws_session_token")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID") or os.getenv("MODEL_ID", "us.anthropic.claude-sonnet-4-5-20250929-v1:0")
print(f"[utils_gen_ai_api] loaded .env from: {ENV_PATH if ENV_PATH.is_file() else f'{ENV_PATH} NOT FOUND'}")
print(f"[utils_gen_ai_api] using MODEL_ID: {MODEL_ID}")

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

    except ClientError as e:
        print(f"[invoke_llm_api] Bedrock ClientError: {e.response.get('Error', {})}")
        return None
    except Exception as e:
        print(f"[invoke_llm_api] {type(e).__name__}: {e}")
        return None
