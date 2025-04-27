from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os
import pandas as pd
from data_ingestion.data_transform import data_convert
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


ASTRADB_ENDPOINT=os.getenv("ASTRADB_ENDPOINT")
ASTRADB_KEYSPACE=os.getenv("ASTRADB_KEYSPACE")
ASTRADB_TOKEN=os.getenv("ASTRADB_TOKEN")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY
os.environ["ASTRADB_ENDPOINT"]=ASTRADB_ENDPOINT
os.environ["ASTRADB_TOKEN"]=ASTRADB_TOKEN
os.environ["ASTRADB_KEYSPACE"]=ASTRADB_KEYSPACE





class ingest_data:
    def __init__(self):
        self.embeddings=GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        self.data_converter=dataconvert()

    def data_ingestion(self):
        vector_store=AstraDBVectorStore(
            embedding=self.embeddings,
            collection_name="Ecomm_chatbot",
            namespace=ASTRADB_KEYSPACE,
            api_endpoint=ASTRADB_ENDPOINT,
            token=ASTRADB_TOKEN,

        )
        storage=status

        if storage==None:
            
            docs=self.data_converter.data_transform()
            inserted_ids=vector_store.add_documents(docs)
            print(inserted_ids)
        else:

            return vector_store

        return vector_store,inserted_ids


            



