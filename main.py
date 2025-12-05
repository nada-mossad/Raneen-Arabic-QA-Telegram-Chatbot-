from fastapi import FastAPI
from pydantic import BaseModel
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import EmbeddingRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack import Document
import pandas as pd
from rapidfuzz import fuzz
import json


app = FastAPI()

df = pd.read_csv(r"Raneen.csv", encoding="utf-8")


documents = []
for _, row in df.iterrows():
    documents.append(
        Document(
            content=row['Formatted'],
            meta={"link": row['link']}
        )
    )


document_store = InMemoryDocumentStore(use_bm25=False, embedding_dim=384)
document_store.write_documents(documents)

retriever = EmbeddingRetriever(
    document_store=document_store,
    embedding_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_format="sentence_transformers"
)


document_store.update_embeddings(retriever)

reader = FARMReader(model_name_or_path="deepset/xlm-roberta-large-squad2", use_gpu=True)
pipe = ExtractiveQAPipeline(reader, retriever)

class Question(BaseModel):
    query: str

@app.post("/ask")
def ask_question(data: Question):
    prediction = pipe.run(query=data.query, params={"Retriever": {"top_k": 3}, "Reader": {"top_k": 1}})

    if not prediction['answers']:
        return {"response": "Sorry, I couldn't find any matching product information."}

    answer = prediction['answers'][0]
    link = answer.meta.get('link', 'Link not found')

    return {
        "question": data.query,
        "answer": answer.answer,
        "product_link": link
    }

