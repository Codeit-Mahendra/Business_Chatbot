from flask import Flask, render_template, jsonify, request
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from huggingface_hub import InferenceClient
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# Set environment variables
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN

embeddings = download_hugging_face_embeddings()

index_name = "business-chatbot" 
# Embed each chunk and upsert the embeddings into your Pinecone index.
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})

# -----------------------------------------------
# Custom LLM class for Hugging Face
# class HuggingFaceLLM:
#     def __init__(self, model_name="microsoft/Phi-3-mini-4k-instruct"):
#         self.model_name = model_name
#         self.client = InferenceClient(token=HUGGINGFACE_API_TOKEN)
    
#     def invoke(self, prompt):
#         response = self.client.text_generation(
#             prompt,
#             model=self.model_name,
#             max_new_tokens=500,
#             temperature=0.7,
#             do_sample=True
#         )
#         return response

# # Initialize Hugging Face LLM
# chatModel = HuggingFaceLLM()

# from langchain_huggingface import HuggingFaceEndpoint

# # Initialize Hugging Face LLM (LangChain compatible)
# chatModel = HuggingFaceEndpoint(
#     repo_id="microsoft/Phi-3-mini-4k-instruct",
#     huggingfacehub_api_token=HUGGINGFACE_API_TOKEN,
#     max_new_tokens=500,
#     temperature=0.7,
#     task="text-generation"
# )

from langchain_openai import ChatOpenAI

chatModel = ChatOpenAI(
    model="llama-3.1-8b-instant",  # Fast and reliable
    openai_api_key=os.getenv("GROQ_API_KEY"),
    openai_api_base="https://api.groq.com/openai/v1",
    max_tokens=500,
    temperature=0.7
)

# --------------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

question_answer_chain = create_stuff_documents_chain(chatModel, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    response = rag_chain.invoke({"input": msg})
    print("Response : ", response["answer"])
    return str(response["answer"])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)