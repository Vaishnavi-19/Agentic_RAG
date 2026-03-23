from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings

load_dotenv()

urls = [
    "https://ocoy.org/read-our-books/introduction-gita-for-awakening/?gad_source=1&gad_campaignid=756548521&gbraid=0AAAAADNGo5MGkfWwP4U_8hnUL5FQcvnH4&gclid=CjwKCAjwg_nNBhAGEiwAiYPYA1xWadfzVHLqp0sq7Qifkr2b3wa1jzHxO0cQUtkCEm_8-img8J3NPBoCJ-cQAvD_BwE",
    "https://www.holy-bhagavad-gita.org/index/",
    "https://www.google.com/search?gs_ssp=eJzj4tTP1TdISa7MSDFg9OJNykhMTyxLTFFIzyxJBABuZAiW&q=bhagavad+gita&oq=Bagvatg&gs_lcrp=EgZjaHJvbWUqDggBEC4YChgLGLEDGIAEMgYIABBFGDkyDggBEC4YChgLGLEDGIAEMgsIAhAAGAoYCxiABDILCAMQABgKGAsYgAQyCwgEEC4YChgLGIAEMgsIBRAAGAoYCxiABDILCAYQABgKGAsYgAQyCwgHEAAYChgLGIAEMgsICBAAGAoYCxiABNIBCTIxOTgxajBqN6gCALACAA&sourceid=chrome&ie=UTF-8",
]

docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=250, chunk_overlap=0
)
doc_splits = text_splitter.split_documents(docs_list)

# vectorstore = Chroma.from_documents(
#     documents=doc_splits,
#     collection_name="rag-chroma",
#     embedding=OpenAIEmbeddings(),
#     persist_directory="./.chroma",
# )

retriever = Chroma(
    collection_name="rag-chroma",
    persist_directory="./.chroma",
    embedding_function=OpenAIEmbeddings(),
).as_retriever()