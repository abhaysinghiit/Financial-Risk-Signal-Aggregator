import requests
class OllamaClient:
    def __init__(self,model='llama3.2',endpoint='http://localhost:11434/api/generate',timeout=180):
        self.model=model; self.endpoint=endpoint; self.timeout=timeout
    def generate(self,prompt):
        try:
            r=requests.post(self.endpoint,json={'model':self.model,'prompt':prompt,'stream':False},timeout=self.timeout)
            r.raise_for_status()
            return r.json()['response']
        except requests.exceptions.ConnectionError:
            return 'Ollama server is not running.'
        except requests.exceptions.Timeout:
            return 'Ollama request timed out.'
        except Exception as e:
            return str(e)
