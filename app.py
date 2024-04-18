from flask import Flask,render_template,jsonify,request
from src.helper import download_hugging_face_embedings
from langchain_community.vectorstores import Pinecone 
import pinecone
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from src.prompt import *
import os

app = Flask(__name__)

load_dotenv()

key = os.getenv("KEY")

embedding = download_hugging_face_embedings()

os.environ['PINECONE_API_KEY'] = key
index_name = "mprbu"

docsearch = Pinecone.from_existing_index(index_name,embedding)

PROMPT = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
chain_type_kwargs = {"prompt": PROMPT}

llm = CTransformers(model="model\llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type = "llama",
                    config={'max_new_tokens':512,'temperature':0.8}
                    )

qa = RetrievalQA.from_chain_type(
    llm = llm,
    chain_type = "stuff",
    retriever = docsearch.as_retriever(search_kwargs={'k':2}),
    chain_type_kwargs=chain_type_kwargs
)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get",methods=["GET","POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result = qa({"query": input})
    print("Response : ",result["result"])
    return str(result["result"])


if __name__ == '__main__':
    app.run(host= "0.0.0.0" , port = "1000" , debug= True)