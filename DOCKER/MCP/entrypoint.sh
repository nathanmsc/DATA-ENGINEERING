#!/bin/bash

# Ativa o ambiente virtual
source /home/mcp/server/.venv/bin/activate

# Inicia o servidor em foreground (para melhor visibilidade de logs)
# O servidor MCP usa transporte streamable-http na porta 3001
exec uv run server.py
