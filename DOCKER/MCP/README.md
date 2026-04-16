# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an MCP (Model Context Protocol) server built with Python using the `mcp` SDK's FastMCP class. It exposes tools, resources, and prompts via streamable HTTP transport.

## Development Commands

**Run the server locally:**
```bash
uv run server.py
```

**Build and run with Docker:**
```bash
docker build -t mcp-server .
docker run -d --name mcp-server -p 3001:3001 mcp-server
```

**Access the running server:**
- Server endpoint: `http://localhost:3001`
- Server logs: `docker logs mcp-server`

**Teste the server (curl):**
```sh
curl -i http://localhost:3001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"jsonrpc": "2.0", "method": "initialize", "id": 1, "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test", "version": "1.0"}}}'
```



**Test the server (Python):**
```python
import requests

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Initialize session
init = requests.post('http://localhost:3001/mcp', headers=headers, json={
    'jsonrpc': '2.0', 'method': 'initialize', 'id': 1,
    'params': {'protocolVersion': '2024-11-05', 'capabilities': {},
               'clientInfo': {'name': 'test', 'version': '1.0'}}
})
session_id = init.headers['Mcp-Session-Id']

# List tools
headers['Mcp-Session-Id'] = session_id
tools = requests.post('http://localhost:3001/mcp', headers=headers, json={
    'jsonrpc': '2.0', 'method': 'tools/list', 'id': 2
})
print(tools.json())

# Call a tool
result = requests.post('http://localhost:3001/mcp', headers=headers, json={
    'jsonrpc': '2.0', 'method': 'tools/call', 'id': 3,
    'params': {'name': 'add', 'arguments': {'a': 5, 'b': 3}}
})
print(result.json())  # Output: 8
```

**Install dependencies:**
```bash
uv sync
```

**Add a new dependency:**
```bash
uv add <package-name>
```

## Architecture

### Server Configuration

The server uses environment variables for configuration (set in `dockerfile`):
- `MCP_HOST`: Bind address (default: `0.0.0.0`)
- `MCP_PORT`: Server port (default: `3001`)

The server runs with `streamable-http` transport, exposing:
- **Tools**: Functions that can be called by MCP clients (e.g., `add`)
- **Resources**: URI-addressable data (e.g., `greeting://{name}`)
- **Prompts**: Template-based prompts (e.g., `greet_user`)

### File Structure

- `server.py`: Main MCP server with FastMCP setup
- `tools/`: Additional tool modules (e.g., `wikipedia.py`)
- `pyproject.toml`: Python project dependencies
- `dockerfile`: Container configuration with `mcp` user
- `entrypoint.sh`: Container startup script

### Transport

The server uses `streamable-http` transport which:
- Runs an HTTP server (powered by uvicorn) on `MCP_HOST:MCP_PORT` (default: `0.0.0.0:3001`)
- Supports JSON responses (configured with `json_response=True`)
- Is stateful by default (sessions maintained in memory)

**Note:** MCP Inspector is not used because it only supports `stdio` transport, not `streamable-http`.

**Important:** When running in Docker, `MCP_HOST` must be `0.0.0.0` to accept connections from outside the container.

### Docker Setup

The container creates an `mcp` user and:
- Installs `uv` for Python package management
- Sets up a virtual environment at `/home/mcp/server/.venv`
- Runs the server as the `mcp` user (not root)
- Exposes the configured MCP port

## Adding New Components

**Add a tool:**
```python
@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"
```

**Add a resource:**
```python
@mcp.resource("myresource://{id}")
def get_resource(id: str) -> str:
    """Resource description"""
    return f"Data for {id}"
```

**Add a prompt:**
```python
@mcp.prompt()
def my_prompt(name: str) -> str:
    """Prompt description"""
    return f"Generate something for {name}"
```
