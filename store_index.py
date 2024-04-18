from src.helper import load_pdf,text_split,download_hugging_face_embedings
#from langchain.vectorstores import Pinecone as PineconeStore
from langchain_community.vectorstores import Pinecone 
import pinecone


from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("KEY")

extracted_data = load_pdf("data/")
text_chunks = text_split(extracted_data)
embedding = download_hugging_face_embedings()


os.environ['PINECONE_API_KEY'] = key
index_name = "mprbu"

docsearch = Pinecone.from_texts(
    [t.page_content for t in text_chunks],
    embedding,
    index_name=index_name
)