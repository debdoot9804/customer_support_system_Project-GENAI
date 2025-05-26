import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from langchain_core.runnables import RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

from langchain_core.prompts import ChatPromptTemplate

from Retriever.retrieval import Retriever

from utils.model_loader import ModelLoader

from prompt_library.prompt import prompt_template

app=FastAPI()
load_dotenv()
app.mount("/static",StaticFiles(directory="static"),name="static")
templates=Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

retriever_obj=Retriever()
modelloader_obj=ModelLoader()

def invoke_chain(query:str):

    retriever=retriever_obj.create_retriever()
    prompt=ChatPromptTemplate.from_template(prompt_template["product_bot"])
    llm=modelloader_obj.load_llm()
    
    chain=(
        {"context":retriever,"question":RunnablePassthrough()}|prompt|llm|StrOutputParser()
    )
    result=chain.invoke(query)
    return result

@app.get("/",response_class=HTMLResponse)
async def index(request:Request):
    return templates.TemplateResponse("chat.html",{"request":request})


@app.post("/get",response_class=HTMLResponse)
async def chat(msg:str=Form(...)):
    result=invoke_chain(msg)
    print(f"Response: {result}")
    return result                            #Returns result to HTML form


    



