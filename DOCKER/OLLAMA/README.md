## MSC/OLLAMA

### Build image from docker file
```sh
docker build -t msc/ollama .
```
### Run docker from image msc/ollama
```sh
docker run -it -d --name ollama-server --hostname ollama-server --restart=always -p 11434:11434 msc/ollama
```
### Download llm model
```sh
ollama pull llama3.1:8b 
```
### Run model
```sh
ollama run llama3.1:8b
```

### API
```sh
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1",
  "prompt":"Why is the sky blue?"
}'

curl http://localhost:11434/api/chat -d '{
  "model": "llama3.1",
  "messages": [
    { "role": "user", "content": "why is the sky blue?" }
  ]
}'

```

### Ollama/Ollama Docker Image Run CPU
```sh
docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```

### Ollama/Ollama Docker Image Run GPU
```sh
docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
```
### OPENWEBUI
```sh
docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

sudo docker run -d --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui --restart always ghcr.io/open-webui/open-webui:main
```
https://github.com/pyspark-ai/pyspark-ai
https://docs.openwebui.com/getting-started/
https://hub.asimov.academy/tutorial/rodando-modelos-de-linguagem-natural-localmente-com-ollama/
https://python.langchain.com/docs/integrations/llms/ollama/
https://www.youtube.com/watch?v=vsIsvcKA7M4
