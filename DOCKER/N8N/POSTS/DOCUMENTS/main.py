import requests
import json


def query_llm(model: str, prompt: str):
    '''
    Send prompt to a locally running llm model.
    Requires the Ollama server to be running:
        llm run <model>
    '''
    
    url = 'http://localhost:11434/api/generate'

    payload = {
        'model': model,
        'prompt': prompt,
        'stream': False,
        'temperature': 0.7
    }

    response = requests.post(url, json=payload)
    response = raise_for_status()
    return data.get('response', '')


def main():
    model = 'llama.3.2:1b'
    prompt = str(input('Prompt: '))
    reply = query_llm(model, prompt)
    print('Model reply\n', reply)


if __name__ == "__main__":
    main()
