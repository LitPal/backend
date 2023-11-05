import os
import openai

import pinecone
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents




def split_docs(documents, chunk_size=1000, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs = text_splitter.split_documents(documents)
  return docs


def get_similar_docs(query, k=3, score=False):  # we can control k value to get no. of context with respect to question.
  if score:
    similar_docs = index.similarity_search_with_score(query, k=k)
  else:
    similar_docs = index.similarity_search(query, k=k)
  return similar_docs

openai.api_key = "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"

documents = load_docs("data")
docs = split_docs(documents)

embeddings = OpenAIEmbeddings(model_name="ada")
query_result = embeddings.embed_query("Hello world")

pinecone.init(
    api_key="b3c95e66-d3bc-41fc-ae63-21dcd3f36212",
    environment="us-west4-gcp-free"
)
index_name = "hacksc"
index = Pinecone.from_documents(docs, embeddings, index_name=index_name)

# from langchain.llm import AzureOpenAI
model_name = "text-davinci-003"
# llm = AzureOpenAI(model_name=model_name)

# chain = load_qa_chain(llm, chain_type="stuff") #we can use map_reduce chain_type also.

def get_answer(query):
    similar_docs = get_similar_docs(query)
    prompt = f"""
            You are reading a mentor chatbot. The chatbot is designed to help you with questions about the research paper.
            Response should be very similar to the original paper. But also simplified to help the mentee understand the paper.
            Below is a query I received from the mentee:
            {query}

            Below is {len(similar_docs)} paragraphs from the document that give context to the solution:
        """
    for docs in similar_docs:
        prompt += docs.page_content + "\n"
    
    prompt += "\n"
    
    prompt += """
        Please write the best response that I should send to this prospect, and also don't make it too long:

        """
    answer = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{
        "role" : "user", "content" : prompt
    }])
#   answer = chain.run(input_documents=similar_docs, question=query)
    return answer
