import os
from mcp.server.fastmcp import FastMCP

# 🔧 configuração via ENV (Docker-friendly)
HOST = os.environ.get("MCP_HOST", "0.0.0.0")
PORT = int(os.environ.get("MCP_PORT", "3001"))

# 🧠 cria servidor MCP
mcp = FastMCP(
    "wiki",
    host=HOST,
    port=PORT,
    json_response=True
)

# 🔧 tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# 📦 resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# 💬 prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# ▶️ start server
if __name__ == "__main__":
    print(f"🚀 MCP Server rodando em http://{HOST}:{PORT}")
    mcp.run(transport="streamable-http")
