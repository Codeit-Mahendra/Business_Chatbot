from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from dotenv import load_dotenv
import os
from pinecone import Pinecone 
from pinecone import ServerlessSpec 
from langchain_pinecone import PineconeVectorStore
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.helper import load_pdf_files, filter_to_minimal_docs, text_split, download_hugging_face_embeddings

load_dotenv()  # Load environment variables from .env file

# Get environment variables for API keys and model configuration
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

# Set environment variables for external services
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACE_API_TOKEN

# Load PDF documents from data directory
extracted_documents = load_pdf_files("E:/7. ML practise Daily/7. GEN AI/11. Chatbot_Github_end to end/Business_Chatbot/data")

# Filter documents to keep only essential metadata (source and content)
minimal_documents = filter_to_minimal_docs(extracted_documents)

# Split documents into smaller text chunks for processing
texts_chunk = text_split(minimal_documents)

# Initialize Hugging Face embeddings model
embeddings = download_hugging_face_embeddings()

# Set up Pinecone client and create vector index
pinecone__api_key = PINECONE_API_KEY
pc = Pinecone(api_key=pinecone__api_key)  # Fixed parameter name

index_name = "business-chatbot"

# Create Pinecone index if it doesn't exist
if not pc.has_indexes():  # Should be pc.has_index(index_name)
    pc.create_index(
        name=index_name,
        dimension=384,  # Embedding dimension
        metric="cosine",  # Similarity metric
        serverless=ServerlessSpec(cloud="aws", region="us-east-1"),  # Serverless configuration
    )

# Get the created index and store document embeddings
index = pc.get_index(index_name)
docsearch = PineconeVectorStore.from_documents(
    documents=texts_chunk,  # Text chunks to vectorize
    embedding=embeddings,   # Embedding model
    index_name=index_name,  # Pinecone index name
)

# This code loads PDFs, processes them into chunks, creates embeddings, and stores them in Pinecone vector database for retrieval