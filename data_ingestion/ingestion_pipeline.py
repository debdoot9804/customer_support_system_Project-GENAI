import os
import pandas as pd
from dotenv import load_dotenv
from typing import List,Tuple
from langchain_core.documents import Document
from langchain_astradb import AstraDBVectorStore
from utils.model_loader import ModelLoader
from config.config_loader import load_config

class DataIngestion:
    """Class for data ingestion"""

    def __init__(self):
        """Initialize env variables,embed model,set CSV file path"""
            
        self.model_loader=ModelLoader()
        self.load_env_variables()
        self.csv_path=self.get_csv_path()
        self.product_data=self.load_csv()
        self.config=load_config()



    def load_env_variables(self):
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

    def get_csv_path(self):
        """gets path to csv file"""

        current_dir=os.getcwd()
        csv_path=os.path.join(current_dir,"data","amazon_product_review.csv")

        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
        
        return csv_path

    def load_csv(self):
        """Load product data from csv"""
        df=pd.read_csv(self.csv_path)  
        columns=['product_title','rating','summary','review']
        if not all(col in df.columns for col in columns):
            raise ValueError(f"CSV file must contain columns: {columns}")
        print(f"Loaded {len(df)} rows")
        return df
    
    def transform_data(self):
        """Transform data to document objects"""
        product_list=[]
        for i,row in self.product_data.iterrows():
            object={
                "product_name":row['product_title'],
                "product_rating":row['rating'],
                "product_summary":row['summary'],
                "product_review":row['review']

            }
            product_list.append(object)
        #print("product list -----")    
        #print(product_list)
        docs=[]
        for entry in product_list:
            metadata={"product_name":entry['product_name'],
                      "product_rating":entry['product_rating'],
                      "product_summary":entry['product_summary'],
                      }
            doc=Document(page_content=entry['product_review'],metadata=metadata)
            docs.append(doc)
        print(f"Transformed {len(docs)} documents")
        return docs

    def store_in_vector_db(self,docs:List[Document]):
        """Store documents in vector database"""
        collection_name=self.config["astra_db"]["collection_name"]
        vector_store=AstraDBVectorStore(
            embedding=self.model_loader.load_embeddings(),
            collection_name=collection_name,
            api_endpoint=self.ASTRADB_ENDPOINT,
            namespace=self.ASTRADB_KEYSPACE,
            token=self.ASTRADB_TOKEN

        )
        inserted_ids=vector_store.add_documents(docs)
        print(f"Inserted {len(inserted_ids)} documents into vector store")
        return vector_store,inserted_ids
    
    

            

    def run_pipeline(self):
        """Run ingestion pipeline"""
        documents=self.transform_data()
        vector_store,inserted_ids=self.store_in_vector_db(documents)

        # query="Suggest me low budget headphones"
        # results=vector_store.similarity_search(query)

        # print(f"\n Search results for query : {query}")
        # for i in results:
        #     print(f"Metadata:{i.metadata} \nContent:{i.page_content}\n")

if __name__ == "__main__":
    ingestion = DataIngestion()
    ingestion.run_pipeline()
            




        
