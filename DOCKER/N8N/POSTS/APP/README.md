```sh
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
uv init app
cd app
uv venv
source .venv/bin/activate
```

### INIT PROJECT

```sh
uv tool install crewai
crewai create crew app
```
### PROJECT
```sh
.
├── knowledge
├── src
│   ├── README.md
│   └── app
│       ├── __init__.py
│       ├── config
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       ├── crew.py
│       ├── main.py
│       └── tools
│           └── __init__.py
└── tests
```

