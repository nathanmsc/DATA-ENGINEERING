### INSTALL UVICORN
```sh
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && sudo apt install -y nodejs
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### INIT PROJECT
```sh
uv tool install crewai
crewai create crew app
```

### PYPROJECT FILE
```toml
#app/pyproject.toml
[project]
name = "app"
version = "0.1.0"
description = "APP using crewAI"
authors = [{ name = "Your Name", email = "you@example.com" }]
requires-python = ">=3.10,<3.14"
dependencies = [
    "crewai[tools]>=0.193.2,<1.0.0"
]

[project.scripts]
app = "app.main:run"
run_crew = "app.main:run"
train = "app.main:train"
replay = "app.main:replay"
test = "app.main:test"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.crewai]
type = "crew"
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

### uv venv
```sh
uv venv
source .venv/bin/activate
```

### CREW RUN
```sh
crewai install
crewai run
```
