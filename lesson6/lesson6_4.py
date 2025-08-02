import requests
from pprint import pprint
from rich.markdown import Markdown
from rich.console import Console

def print_markdown_response(response: str):
    console = Console()
    md = Markdown(response)
    console.print(md)
    
def generate_with_ollama(prompt:str):
    url = 'http://localhost:11434/api/generate'
    payload = {
        "model":"gemma3:1b",
        "prompt" : prompt,
        "stream" : False
    }
    
    response = requests.post(url, json = payload)
    result =response.json()
    print("===========AI回應==============")
    print_markdown_response(result['response'])
    
generate_with_ollama("請用簡單的方式解釋什麼是Python的函式？")
