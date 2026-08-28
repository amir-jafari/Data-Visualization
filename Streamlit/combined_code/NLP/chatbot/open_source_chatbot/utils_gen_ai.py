import torch
from transformers import pipeline
# langchain >=1.0 removed the top-level `PromptTemplate`/`LLMChain` shortcuts and moved
# HuggingFacePipeline out of `langchain.llms` into the separate `langchain_huggingface`
# integration package. LCEL (the `prompt | llm` pipe syntax) replaces LLMChain.
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import HuggingFacePipeline
import  streamlit as st
# databricks/dolly-v2-7b (and the rest of the dolly-v2 line) has been gated/archived
# on the Hub -- it 401s even on an unauthenticated HEAD request now. Swapped for a
# similarly-sized, currently-public instruct model. Phi-3 is natively supported in
# transformers now, so trust_remote_code=True would load the model repo's own stale
# custom modeling code instead of the maintained built-in implementation -- dropped it.
generate_text = pipeline(model="microsoft/Phi-3-mini-4k-instruct", dtype=torch.bfloat16,
                         device_map="auto", return_full_text=True)

prompt = PromptTemplate(
    input_variables=["instruction"],
    template="{instruction}")

prompt_with_context = PromptTemplate(
    input_variables=["instruction", "context"],
    template="{instruction}\n\nInput:\n{context}")

hf_pipeline = HuggingFacePipeline(pipeline=generate_text)

def gen_ai(context=None, prompt=None):

    if not context:
        llm_context_chain = prompt_with_context | hf_pipeline
        answer = llm_context_chain.invoke({"instruction": f"{prompt}", "context": context}).lstrip()

    else:
        llm_chain = prompt | hf_pipeline
        answer = llm_chain.invoke({"instruction": f"{prompt}"}).lstrip()

    return  answer


def side_bar():
    with st.sidebar:
        if st.button('Clear Chat'):
            # Clear the chat history
            st.session_state.messages = []