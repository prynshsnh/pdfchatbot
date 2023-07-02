import streamlit as st
from langchain.embeddings.cohere import CohereEmbeddings
from langchain.llms import Cohere
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.vectorstores import Qdrant
import os
import random
import textwrap as tr


from my_pdf_lib import text_to_docs, parse_pdf
from db_chat import user_message, bot_message

cohere_api_key = os.environ.get('priyanshusinha')

st.title("T. M. Riddle's Diary 🪄")
st.info(
    "Developed by [Priyanshu Sinha](https://priyanshusinha.online/), the boy who lifted 💪🏼."
)

pages = None

uploaded_file = st.file_uploader(
    "**Upload a pdf file :**",
    type=["pdf"],
)
if uploaded_file:
    doc = parse_pdf(uploaded_file)
    pages = text_to_docs(doc)

page_holder = st.empty()

prompt_template = """Role: Technical Assistant that is an expert in reading research papers and documentation

Text: {context}

Question: {question}

Answer the question based on the text provided. If the text doesn't contain the answer, reply that the answer is not available."""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)
chain_type_kwargs = {"prompt": PROMPT}

prompt = st.session_state.get("prompt", None)

if prompt is None:
    prompt = [{"role": "system", "content": prompt_template}]

for message in prompt:
    if message["role"] == "user":
        user_message(message["content"])
    elif message["role"] == "assistant":
        bot_message(message["content"], bot_name="Tom Riddle")

if pages:
    with page_holder.expander("File Content", expanded=False):
        pages
    embeddings = CohereEmbeddings(
        model="multilingual-22-12", cohere_api_key=cohere_api_key
    )
    store = Qdrant.from_documents(
        pages,
        embeddings,
        location=":memory:",
        collection_name="my_documents",
        distance_func="Dot",
    )
    col1, col2 = st.columns(2)
    messages_container = st.container()
    question = col1.text_input(
        "", placeholder="Type your query here", label_visibility="collapsed"
    )

    if col2.button("Run", type="secondary"):
        prompt.append({"role": "user", "content": question})
        chain_type_kwargs = {"prompt": PROMPT}
        with messages_container:
            user_message(question)
            botmsg = bot_message("...", bot_name="Tom Riddle")

        qa = RetrievalQA.from_chain_type(
            llm=Cohere(model="command", temperature=0, cohere_api_key=cohere_api_key),
            chain_type="stuff",
            retriever=store.as_retriever(),
            chain_type_kwargs=chain_type_kwargs,
            return_source_documents=True,
        )

        answer = qa({"query": question})
        result = answer["result"].replace("\n", "").replace("Answer:", "")

        with st.spinner("Loading response ..."):
            botmsg.update(result)

        prompt.append({"role": "assistant", "content": result})

    st.session_state["prompt"] = prompt
else:
    st.session_state["prompt"] = None
    st.warning("No file found. Upload a file to chat!")