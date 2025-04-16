# %% ----- Imports
import os
import boto3
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv

# %% ----- Configuration
load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("aws_access_key_id")
AWS_SECRET_ACCESS_KEY = os.getenv("aws_secret_access_key")
AWS_SESSION_TOKEN = os.getenv("aws_session_token")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0")

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
        return None
    except Exception as e:
        return None
