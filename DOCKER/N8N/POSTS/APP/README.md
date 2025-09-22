```sh
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && apt install -y nodejs
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv init app
cd app
uv venv
source .venv/bin/activate
```
