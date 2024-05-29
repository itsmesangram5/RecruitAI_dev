from flask import jsonify
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class AddScore:    
    def add_score(self):
        loader = CSVLoader(file_path='resources\clg_ranking.csv')
        data = loader.load()
        clg_name="DY Patil institute of engineering management and research Akurdi Computer Engineering"
        faiss_index = FAISS.from_documents(data, OpenAIEmbeddings())
        docs = faiss_index.similarity_search(clg_name, k=1)
        print(type(docs))
        data_row=docs[0]
        row_number = data_row.metadata['row']
        percentage_clg=((1795-row_number)*100)/1795
        
        
        loader = CSVLoader(file_path='resources\company_ranking.csv')
        data = loader.load()
        company_name="Google"
        faiss_index1 = FAISS.from_documents(data, OpenAIEmbeddings())
        docs1 = faiss_index1.similarity_search(company_name, k=1)
        print(type(docs1))
        data_row1=docs1[0]
        row_number1 = data_row1.metadata['row']
        percentage_comp=((9057-row_number1)*100)/9057
        
        print(percentage_comp)
        return jsonify({"message": percentage_clg}), 200
