from .ollama_client import OllamaClient
client=OllamaClient()
def generate_executive_summary(results):
    body=''
    for r in results:
        s=r['score']
        body+=f"Customer:{s['CustomerID']} Risk:{s['RiskScore']} Level:{s['RiskLevel']}\n{s['Signals']}\n{r['summary']}\n\n"
    prompt='Summarize the following customer investigations into an executive report with Overall Risk Landscape, Common Patterns, Highest Priority Customers, and Immediate Actions.\n\n'+body
    return client.generate(prompt)
