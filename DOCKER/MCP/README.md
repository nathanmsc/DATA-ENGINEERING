apt update -y

curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv init mcp
cd mcp
uv venv
source .venv/bin/activate

uv add "mcp[cli]"
uv run mcp

from.server.fastmcp import FastMCP

mcp = FastMCP('MCPServer')

if __name__ == '__main__':
    mcp.run

mcp run server.py

