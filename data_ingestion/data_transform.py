import pandas as pd
from langchain_core.documents import Document

class data_convert:
    def __init__(self):
        print("data convert has init")
        self.product_data=pd.read_csv("data\\amazon_product_review.csv")
        print(self.product_data.head())
    def data_transform(self):
        col=self.product_data.columns
        req_col=list(col[1:])
        print(req_col)
        product_list=[]
        for index,row in self.product_data.iterrows():
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
        print(docs[0])
            

if __name__=="__main__":
    converter=data_convert()  
    converter.data_transform()  
