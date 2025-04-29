import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from config.config_loader import load_config

class ModelLoader:
    """For loading embedding models & LLM models"""

    def __init__(self):
        load_dotenv()
        self._validate_env()
        self.config=load_config()

    def _validate_env(self):
        """Validate env variables"""
        required=["GOOGLE_API_KEY"] 
        missing=[i for i in required if not os.getenv(i)]
        if missing:
            raise EnvironmentError("Missing env variables: ",{missing})
        
    def load_embeddings(self):
        """Load & return embedding model"""
        print("Loading Embedding model")
        model_name=self.config['embedding_model']['model_name']    
        return GoogleGenerativeAIEmbeddings(model=model_name)
    
    def load_llm(self):
        """Loading LLM & return"""
        model_name=self.config['llm']['model_name']


        return ChatGoogleGenerativeAI(model=model_name)
    
                                      

           
