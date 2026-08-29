"""
The local-model half of the open-source chatbot.

Everything here runs on this machine -- no API, no AWS keys. The model is
loaded once by load_pipeline() and reused; see 01_basics/10_state_and_config/
06_caching.py for what @st.cache_resource is doing.
"""

import torch
from transformers import pipeline
# langchain >=1.0 removed the top-level `PromptTemplate`/`LLMChain` shortcuts and moved
# HuggingFacePipeline out of `langchain.llms` into the separate `langchain_huggingface`
# integration package. LCEL (the `prompt | llm` pipe syntax) replaces LLMChain.
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_huggingface import HuggingFacePipeline
import streamlit as st

MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"

instruction_prompt = PromptTemplate(
    input_variables=["instruction"],
    template="{instruction}")

prompt_with_context = PromptTemplate(
    input_variables=["instruction", "context"],
    template="{instruction}\n\nInput:\n{context}")


@st.cache_resource(show_spinner=f"Loading {MODEL_NAME} -- slow the first time...")
def load_pipeline():
    """Load the model once per session, not on every rerun or app switch.

    Without the cache this runs at import time, and the launcher purges this
    module whenever you switch apps -- so a multi-GB model would be reloaded
    every single time you came back to this page.

    databricks/dolly-v2-7b (and the rest of the dolly-v2 line) has been
    gated/archived on the Hub -- it 401s even on an unauthenticated HEAD
    request now. Swapped for a similarly-sized, currently-public instruct
    model. Phi-3 is natively supported in transformers now, so
    trust_remote_code=True would load the model repo's own stale custom
    modeling code instead of the maintained built-in implementation -- dropped.
    return_full_text=False so the pipeline returns only the new completion,
    not the formatted prompt echoed back; max_new_tokens bounds runaway
    generations.
    """
    return pipeline(model=MODEL_NAME, dtype=torch.bfloat16, device_map="auto",
                    return_full_text=False, max_new_tokens=512)


def _to_chat_format(prompt_value):
    # Phi-3 is chat-template-tuned; handing it raw, unstructured text (rather than a
    # properly formatted <|user|>...<|assistant|> turn) leads it to free-continue the
    # text instead of treating it as something to respond to.
    text = prompt_value.to_string() if hasattr(prompt_value, "to_string") else str(prompt_value)
    return load_pipeline().tokenizer.apply_chat_template(
        [{"role": "user", "content": text}],
        tokenize=False,
        add_generation_prompt=True,
    )


to_chat = RunnableLambda(_to_chat_format)


def gen_ai(context=None, prompt=None):
    """Answer `prompt`, optionally grounded in `context`."""
    hf_pipeline = HuggingFacePipeline(pipeline=load_pipeline())

    if not context:
        llm_chain = instruction_prompt | to_chat | hf_pipeline
        answer = llm_chain.invoke({"instruction": f"{prompt}"}).lstrip()
    else:
        llm_context_chain = prompt_with_context | to_chat | hf_pipeline
        answer = llm_context_chain.invoke({"instruction": f"{prompt}",
                                           "context": context}).lstrip()

    return answer


def side_bar():
    with st.sidebar:
        if st.button('Clear Chat'):
            # Clear the chat history
            st.session_state.messages = []
