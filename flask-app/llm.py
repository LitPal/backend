# general LLM file

import os 
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain.llms import HuggingFacePipeline
from langchain.llms import HuggingFaceHub

import tempfile
import huggingface_hub
import transformers
import requests
from transformers import pipeline
# import base64
import chromadb
chroma_client = chromadb.Client()





def getPDF(url: str):
    # post a get req to obtain the
    query_parameters = {"downloadformat": "pdf"}
    response = requests.get(url, params=query_parameters)

    with open("test.pdf", mode="wb") as file:
        file.write(response.content)
    
    return "test.pdf"

class LLM:
    # create the model based on a selected pdf
    def __init__(self, url: str) -> None:
        self.url = url

        # turn the url into a pdf, and store it as a data member
        self.pdf = getPDF(url)


        # our stored LLM that we use for querying
        self.llm1 = OpenAI(openai_api_key="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")

        # optional: toggle this model as an alternative
        repo_id = "Salesforce/xgen-7b-8k-base" # "impira/layoutlm-document-qa"
        self.llm2 = HuggingFaceHub(
            repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
        )

        # choose the LLM that we will use
        self.llm_model = self.llm1

        self.db = None
        self.init_db(self.pdf)

    
    def init_db(self, file):
        # load document
        loader = PyPDFLoader(file)
        documents = loader.load()
        # split the documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)

        # select which embeddings we want to use
        embeddings = OpenAIEmbeddings(openai_api_key="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") # "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")

        # create the vectorestore to use as the index
        self.db = Chroma.from_documents(texts, embeddings)

        return self.db

        
        

    # query ourself for the result and return it
    def query(self, question: str, k=2):

        retriever = self.db.as_retriever(search_type="similarity", search_kwargs={"k": k})

        # create a chain to answer questions 
        qa = RetrievalQA.from_chain_type(
            llm=self.llm_model,
            chain_type="map_reduce",
            retriever=retriever,
            return_source_documents=True
        )
    
        result = qa({"query": question})
        print(result['result'])
        return result

