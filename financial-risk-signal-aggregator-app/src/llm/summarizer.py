from .retriever import retrieve_relevant_news
from .prompt_builder import build_prompt
from .ollama_client import OllamaClient
client=OllamaClient()
def generate_customer_summary(customer,score,alerts,news_text):
    news=retrieve_relevant_news(customer,score,alerts,news_text)
    return client.generate(build_prompt(customer,score,alerts,news))
