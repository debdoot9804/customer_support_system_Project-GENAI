from langchain_astradb import AstraDBVectorStore
from typing import List
from config.config_loader import load_config
from utils.model_loader import ModelLoader
from dotenv import load_dotenv
import os

load_dotenv()

class Retriever:
    def __init__(self):
        pass

    def load_env_variable(self):
        pass

    def load_retriever(self):
        pass

    def call_retriever(self),query:str->List[Document]:
        pass



if __name__=="__main__":
    obj=Retriever()
    query="Suggest some top end laptops"
    results=obj.call_retriever(query)

    for ids,doc in enumerate(results):
        print(f"Results {ids}: {doc.page_content}\n Metadata: {doc.metadata} \n")
        



