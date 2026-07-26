from functools import lru_cache
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def split_articles(news_text):
    return [a.strip() for a in news_text.split('=== ARTICLE') if a.strip()]

@lru_cache(maxsize=16)
def cached_news_embeddings(news_text):
    model=get_model()
    articles=split_articles(news_text)
    emb=model.encode(articles)
    return articles,emb

def retrieve_relevant_news(customer,score,alerts,news_text,top_k=3):
    articles,emb=cached_news_embeddings(news_text)
    model=get_model()
    alert_text=' '.join(a.get('Description','') for a in alerts if a.get('CustomerID')==customer['CustomerID'])
    query=f"{score['Signals']} {customer['Country']} {customer['RiskCategory']} {customer['PEP']} {alert_text}"
    q=model.encode([query])
    sims=cosine_similarity(q,emb)[0]
    idx=np.argsort(sims)[::-1][:top_k]
    return [articles[i] for i in idx]
