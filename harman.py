from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import FAISS 
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from dotenv import load_dotenv


load_dotenv()

#1 Vectorize Code
loader = CSVLoader(file_path="Hackathon.csv")
documents = loader.load()

embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(documents, embeddings)


#2 Function for similarity search
def retrieve_info(query):
    similar_response = db.search(query, k=3)
    
    page_contents_array = [doc.page_content for doc in similar_response]
    
    print(page_contents_array)
    return page_contents_array

#3 Setup LLMChain & Prompts
llm = ChatOpenAI(temperatur =0, model = "gpt-3.5-turbo-16k-0613")
template = """ 
You are reading a mentor chatbot. The chatbot is 
designed to help you with questions about the research paper.
Response should be very similar to the original paper. But also simplified to help the mentee understand the paper.

Below is a message I received from the mentee.:
{message}

Below is the response I generated:
{response}
Please write the best response that I should send to this prospect:
"""

prompt = PromptTemplate(
	input_variable = ["message", "response"],
	template = template
)

chain = LLMChain(llm=llm, prompt=prompt)

#4 Retrieve augmented gen

def generate_response(message):
    response = retrieve_info(message)
    final = chain.run(message=message, response=response)
    return final

message = """

What really is a neural network
"""

final = generate_response(message)
print(final)
