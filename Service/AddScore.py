from flask import jsonify
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class AddScore:    
    def add_score(self):
        loader = CSVLoader(file_path='resources\clg_ranking.csv')
        data = loader.load()
        txt="DY Patil institute of engineering management and research Akurdi Computer Engineering"
        faiss_index = FAISS.from_documents(data, OpenAIEmbeddings())
        docs = faiss_index.similarity_search(txt, k=1)
        print(type(docs))
        data_row=docs[0]
        row_number = data_row.metadata['row']
        percentage_clg=((1795-row_number)*100)/1795
        return jsonify({"message": percentage_clg}), 200
