## OLLAMA

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