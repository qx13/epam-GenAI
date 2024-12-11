import os
import re

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI
from langchain.schema import StrOutputParser
from langchain_community.document_loaders import RecursiveUrlLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint
from langserve import add_routes

load_dotenv()

HUGGINGFACEHUB_API_TOKEN = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
LINK_SITE = os.environ.get("LINK_SITE")


# extractor for page content
def bs4_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    return re.sub(r"\n\n+", "\n\n", soup.text).strip()


loader = RecursiveUrlLoader(LINK_SITE, extractor=bs4_extractor)

# initialize HF LLM
hf_llm = HuggingFaceEndpoint(repo_id="meta-llama/Meta-Llama-3-8B-Instruct")

template = """
Develop a convincing thesis that clearly articulates the main idea based on the text.
The answer should be brief, contain no arguments, contain no reflections, contain no explanations.


text: {text}


Answer: The thesis is ...
"""
prompt = ChatPromptTemplate.from_template(template)

chain = prompt | hf_llm | StrOutputParser()

# limit the number of articles

MAX_COUNT_READ = os.environ.get("MAX_COUNT")
MAX_COUNT = int(MAX_COUNT_READ) if MAX_COUNT_READ else 10000
MAX_TEX_SIZE = 30000

count = 0

posts = []

# lazy_load will allow you to process them one at a time, rather than all at once
for doc in loader.lazy_load():
    # whether the text does not exceed the maximum number of tokens
    if len(doc.page_content) > MAX_TEX_SIZE:
        continue
    doc.page_content = chain.invoke(doc.page_content)
    posts.append(doc)
    # comment out this section of code if you need to process everything
    count += 1
    if count >= MAX_COUNT:
        break
    # comment out this section of code if you need to process everything

embeddings = HuggingFaceEmbeddings(
    model_name="cointegrated/LaBSE-en-ru", model_kwargs={"device": "cpu"}
)

# vector db
db = FAISS.from_documents(posts, embeddings)

db.save_local("faiss_news_db")

# creat retriever
retriever = db.as_retriever(
    search_type="similarity",
    k=4,
    score_threshold=None,
)


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

add_routes(app, retriever)

# run server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8501)
