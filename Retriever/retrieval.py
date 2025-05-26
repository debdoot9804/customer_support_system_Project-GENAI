from langchain_astradb import AstraDBVectorStore
from typing import List
from config.config_loader import load_config
from langchain_core.documents import Document
from utils.model_loader import ModelLoader
from dotenv import load_dotenv
import os

load_dotenv()

class Retriever:
    def __init__(self):
        self.ModelLoader=ModelLoader()
        self.config=load_config()
        self.load_env_variable()
        self.vector_store=None
        self.retriever=None

    def load_env_variable(self):
        """load & validate env variables"""
        print(f"\n Loading env variables")
        load_dotenv()
        required=["ASTRADB_ENDPOINT","ASTRADB_KEYSPACE","ASTRADB_TOKEN","GOOGLE_API_KEY"]
        missing=[i for i in required if not os.getenv(i)]
        if missing:
            raise EnvironmentError("Missing env variables: ",{missing})
        
        self.GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
        self.ASTRADB_ENDPOINT=os.getenv("ASTRADB_ENDPOINT")
        self.ASTRADB_KEYSPACE=os.getenv("ASTRADB_KEYSPACE")
        self.ASTRADB_TOKEN=os.getenv("ASTRADB_TOKEN")

    def create_retriever(self):
        if not self.vector_store:
            collection_name=self.config["astra_db"]["collection_name"]

            self.vector_store=AstraDBVectorStore(
            embedding=self.ModelLoader.load_embeddings(),
            collection_name=collection_name,
            api_endpoint=self.ASTRADB_ENDPOINT,
            namespace=self.ASTRADB_KEYSPACE,
            token=self.ASTRADB_TOKEN
            )
        if not self.retriever:
            top_k=self.config["retriever"]["top_k"] if "retriever" in self.config else 3   #Fall back conition to return 3 results if not provided in config file
            retriever=self.vector_store.as_retriever(search_kwargs={"k":top_k})
            print("Retriever loaded successfully")
            return retriever




    def call_retriever(self,query:str)->List[Document]:
        retriever=self.create_retriever()
        result=retriever.invoke(query)
        return result



if __name__=="__main__":
    obj=Retriever()
    query="Suggest some high end laptops"
    results=obj.call_retriever(query)

    for ids,doc in enumerate(results,1):
        print(f"Results {ids}: {doc.page_content}\n Metadata: {doc.metadata} \n")




