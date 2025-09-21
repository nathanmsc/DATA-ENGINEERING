## 📌 Automação de Postagens no Instagram com n8n + Ollama + Google API

### 🔧 Ferramentas Utilizadas

* n8n → Orquestração da automação

* Docker → Containers para n8n e Ollama

* Ollama → Geração de textos criativos (captions, hashtags, descrições) com IA local

* Instagram Graph API → Postagem automática

* Google Drive API → Integração com:

  * Google Docs (documentos de briefing, rascunhos de postagens)

  * Google Sheets (planejamento de calendário de postagens)

  * Google Writer & Calc (edição colaborativa de conteúdo)
  

### STEPS

#### Build N8N Container

```sh
docker run -it --restart always --name n8n-server --hostname n8n-server -e GENERIC_TIMEZONE="America/Sao_Paulo" -v volume:/home/node/.n8n --net network-net --ip 172.19.0.2 -p 5678:5678 -d n8nio/n8n:latest
```

#### Build Ollama Container

```sh
docker run -it --restart always --name ollama-server --hostname ollama-server -v setup:/home/ollama --net network-net --ip 172.19.0.3 -p 5678:5678 -d mindsetcloud/ollama:latest
```

#### N8N AUTOMATION JSON FILE

[https://github.com/nathanmsc/DATA-ENGINEERING/edit/main/DOCKER/N8N/POSTS/automation.json](https://raw.githubusercontent.com/nathanmsc/DATA-ENGINEERING/refs/heads/main/DOCKER/N8N/POSTS/automation.json)


### 🔑 Google API (Docs, Sheets)

* Criar um projeto no Google Cloud Console

  * Ativar as APIs:

     * Google Drive API

     * Google Docs API

     * Google Sheets API

  * Criar credenciais OAuth e importar no n8n

  * Conectar nodes do n8n às contas do Google

### REFERENCES

* [FREE AI Images Generation N8n Automation](https://www.youtube.com/watch?v=qeYgROvh1gY)
* [Python generate image](https://www.youtube.com/watch?v=-X_d2AVXVkQ)
* [Generate free images](https://www.youtube.com/watch?v=Ic5BRW_nLok)
* [Janus Multimodal](https://www.youtube.com/watch?v=8fNm6LLZ5WY)
* [Instagram Graph API](https://www.youtube.com/watch?v=t5ZgBLn3S3I)
* [N8N Graph API Integration](https://www.youtube.com/watch?v=fabfLv0ooEw)
