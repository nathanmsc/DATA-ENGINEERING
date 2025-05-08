
N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
n8n-nodes-mcp-client

serpAPI
https://www.youtube.com/watch?v=pT32eqHaWj4


npm install -g @modelcontextprotocol/server-brave-search
apt update -y

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv init mcp
cd mcp
uv venv
source .venv/bin/activate

uv add "mcp[cli]"
uv run mcp
```py
from.server.fastmcp import FastMCP

mcp = FastMCP('MCPServer')

if __name__ == '__main__':
    mcp.run
```

```sh
mcp run server.py
```

[n8n-mcp-server](https://huggingface.co/blog/lynn-mikami/n8n-mcp-server)
[n8n-nodes-mcp](https://github.com/nerding-io/n8n-nodes-mcp)
