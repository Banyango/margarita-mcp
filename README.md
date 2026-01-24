# ReciMCP

A MCP recipe management application. 

This repository contains application code under `src/` grouped into `app/`, `core/`, and `libs/` modules.

Key ideas
- `src/app` — application wiring, API surface and configuration
- `src/core` — business logic (commands, interfaces, queries)
- `src/libs` — infrastructure code (persistence, external clients)

Requirements
- Python 3.11+ (project bytecode indicates 3.12 compatibility; 3.11+ recommended)

Quickstart

1. Create and activate a virtual environment (macOS / zsh):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies

- If you use Poetry:

```bash
poetry install
```

- Otherwise, if there is a `requirements.txt` or you prefer pip editable install:

```bash
pip install -r requirements.txt  # if present
# or
pip install -e .
```

Run the application

- Run the main script (quick run):

```bash
python src/main.py
```

Testing

- Run tests with pytest:

```bash
pytest -q
```

Development notes

- The repository uses a `src/` layout. Keep package imports relative to `src` (e.g. `from app import ...`).
- Common files/directories to ignore are already included in `.gitignore` (virtualenvs, bytecode, editor folders, etc.).

Project structure (high level)
```
src/
  main.py         # entry point
  app/            # API, config, DI container
  core/           # domain logic and interfaces
  libs/           # infra (clients, repositories)
```

Contributing

- Please open an issue for feature requests or bugs, and submit pull requests with a clear description.
- Add unit tests for new behavior and keep changes small.

License & Contact

- Add your preferred license file (e.g. `LICENSE`) if you plan to open-source this project.
- For questions, contact the repository owner or maintainers.

