### ENABLE COMUNITY NODES
```yaml
N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
```
### ADD COMUNITY NODE MCP CLIENT
n8n-nodes-mcp-client

### ADD MCP TOOLS
```npx
npm install -g @modelcontextprotocol/server-brave-search
```
---
### LOCAL MCP SERVER WITH PYTHON
```sh
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && apt install -y nodejs
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv init mcp
cd mcp
uv add mcp "mcp[cli]"
```
### INSTALL REQUIREMENTS
```sh
uv pip install -r requirements.txt
```
---

### SIMPLE MCP SERVER WITH PYTHON
```py
from.server.fastmcp import FastMCP

mcp = FastMCP('MCPServer')

if __name__ == '__main__':
    mcp.run()
```

### RUN LOCAL MCP
```sh
source .venv/bin/activate
uv run server.py
```
---
### REFERÊNCIAS

|Descrição| Link  |
|:----------------:|:-----------------------------------------------------:|
|n8n-mcp-server    |[n8n-mcp-server](https://huggingface.co/blog/lynn-mikami/n8n-mcp-server)|
|n8n-nodes-mcp|[n8n-nodes-mcp](https://github.com/nerding-io/n8n-nodes-mcp)|
|serpAPI|[serpAPI](https://www.youtube.com/watch?v=pT32eqHaWj4)|
||https://www.youtube.com/watch?v=ZqlpCliftQg|
||https://www.youtube.com/watch?v=ZqlpCliftQg|
|MCP Local|https://www.youtube.com/watch?v=03P9Y99bhLo|
