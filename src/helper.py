#from langchain.document_loaders import 
from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
#from langchain.embeddings import HuggingFaceEmbeddings




#extracting daata from the pdf
def load_pdf(data):
    loader = DirectoryLoader(data,glob="*.pdf",loader_cls=PyPDFLoader)

    documents = loader.load()

    return documents



# creating data Chunks

def text_split(extracted_data):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 40,chunk_overlap = 15)
    text_chunks = text_splitter.split_documents(extracted_data)

    return text_chunks 


#downloading embedding model 
def download_hugging_face_embedings():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embeddings