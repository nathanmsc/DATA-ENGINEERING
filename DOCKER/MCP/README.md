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
source .venv/bin/activate
```
### INSTALL REQUIREMENTS
```sh
uv pip install -r requirements.txt
```
---

### SIMPLE MCP SERVER WITH PYTHON
```py
from mcp.server.fastmcp import FastMCP  # Certifique-se de que esse caminho é válido

mcp = FastMCP(
    name='MCPServer',
    host='container-ip',
    port=3001,
    sse_path='/sse/',
)

@mcp.tool()
def list_task(max_results: int) -> list[str]:  # Use List[str] se Python <3.9
    """List all tasks"""
    return [
        'Eat breakfast',
        'Go to the gym',
        'Read a book',
    ][:max_results]

if __name__ == '__main__':
    mcp.run(transport='sse')

```

### RUN LOCAL MCP
```sh
source .venv/bin/activate
uv run server.py
```

```sh
source .venv/bin/activate
python server.py
```
### RUN MCP INSPECTOR
```sh
mcp dev server.py
```
### DOCKER RUN
```sh
 docker run -it --name mcp-server --hostname mcp-server --restart always --net network --ip 172.19.0.35 -p 3001:3001 -p 6274:6274 -p 6277:6277 -d container-image
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
|Local llm with MCP|https://www.youtube.com/watch?v=aiH79Q-LGjY|
