#!/bin/bash

# Ativa o ambiente virtual
source /home/mcp/server/.venv/bin/activate

# Inicia o servidor em segundo plano
nohup uv run server.py > /home/mcp/server/server.log 2>&1 &

# Inicia o inspector também em segundo plano
nohup npx --yes @modelcontextprotocol/inspector > /home/mcp/server/inspector.log 2>&1 &

# Mantém o container vivo (tail bloqueia em foreground)
tail -f /dev/null
