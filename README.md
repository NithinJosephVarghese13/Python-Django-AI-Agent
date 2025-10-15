## Django AI Agent (LangGraph + Ollama + Permit.io + TMDB)

A Django 5 project demonstrating local-first AI agents built with LangGraph and Ollama, with:
- Document CRUD guarded by Permit.io authorization
- A Movie Discovery agent backed by The Movie Database (TMDB)
- A minimal Django app with a `Document` model and Jupyter notebooks showing end-to-end usage

### Features

- Local LLMs via Ollama (`llama3.1:8b` by default) for cost-efficient development
- LangGraph ReAct-style agents and an optional multi-agent supervisor
- Documents toolset: list, search, get, create, update, delete — permission-checked via Permit.io
- Movie toolset: TMDB search and movie detail
- Jupyter notebooks to explore users/permissions, agents, memory, and a supervisor

### Project Structure

```
src/
  ai/
    agents.py              # Creates document & movie agents using LangGraph's ReAct agent
    llms.py                # Configures ChatOllama + Embeddings (local Ollama)
    supervisors.py         # Multi-agent supervisor
    tools/
      documents.py         # Document tools with Permit.io checks
      movie_discovery.py   # TMDB tools (search + detail)
  core/
    settings.py            # Django settings & env config (Ollama, TMDB, Permit, OpenAI)
    urls.py, wsgi.py, asgi.py
  documents/
    models.py              # Document model with owner FK + lifecycle fields
  mypermit/
    client.py              # Permit.io client initialization (PDP + API key required)
  tmdb/
    client.py              # HTTP client for TMDB API
notebook/
  ...                      # Jupyter notebooks (agents, memory, TMDB client, supervisor, etc.)
requirements.txt
```

Key settings and integrations live in `src/core/settings.py`:

```126:134:src/core/settings.py
OPENAI_API_KEY = config("OPENAI_API_KEY", default=None)

TMDB_API_KEY = config("TMDB_API_KEY", default=None)

PERMIT_API_KEY= config("PERMIT_API_KEY", default=None)
PERMIT_PDP_URL= config("PERMIT_PDP_URL", default="https://cloudpdp.api.permit.io")

# Optional: base URL for local Ollama
OLLAMA_BASE_URL = config("OLLAMA_BASE_URL", default="http://localhost:11434")
```

### Requirements

- Python 3.12
- Django 5
- Ollama installed locally and the target models pulled
- API keys:
  - TMDB_API_KEY (required for movie search)
  - PERMIT_API_KEY (required for documents tools; otherwise import will raise)
  - OPENAI_API_KEY (optional; not required for local Ollama)
- Jupyter (for notebooks)

Python deps (from `requirements.txt`):

```
Django>=5.0,<6.0
jupyter
langchain-ollama>=0.1.0
langgraph
langgraph-supervisor
python-decouple
permit
httpx
```

### Setup

1) Create and activate a virtual environment (Windows PowerShell):

```powershell
cd "C:\Programming\Python Django AI Agent"
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2) Configure environment variables. The project uses `python-decouple` to read envs defined in the host environment. You can place a `.env` alongside `src/manage.py` or set system env variables.

Example `.env` (place in `src/` next to `manage.py`):

```
DJANGO_SETTINGS_MODULE=core.settings
SECRET_KEY=dev-only-not-for-prod
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Local Ollama
OLLAMA_BASE_URL=http://localhost:11434

# TMDB
TMDB_API_KEY=YOUR_TMDB_API_KEY

# Permit.io
PERMIT_API_KEY=YOUR_PERMIT_API_KEY
PERMIT_PDP_URL=https://cloudpdp.api.permit.io

# Optional
OPENAI_API_KEY=sk-...
```

3) Install and prepare Ollama with local models:

```bash
# Install Ollama from https://ollama.com
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

4) Initialize the database:

```powershell
cd src
python manage.py migrate
python manage.py createsuperuser
```

5) Run the server:

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/admin/` to access Django Admin.

### Using the Agents

You can interact with the agents either in notebooks or via Django shell. The tools expect a `configurable` (or `metadata`) dict containing the `user_id` so that Permit.io checks can be evaluated.

Django shell example:

```powershell
cd src
python manage.py shell
```

```python
from ai.agents import get_document_agent, get_movie_discovery_agent
from langchain_core.runnables import RunnableConfig

# The user_id should correspond to an existing Django user.
cfg = RunnableConfig(configurable={"user_id": 1})

doc_agent = get_document_agent()
# Example: list documents
resp = doc_agent.invoke({"messages": "List my recent documents"}, cfg)
print(resp)

movie_agent = get_movie_discovery_agent()
resp = movie_agent.invoke({"messages": "Search for sci-fi movies from the 90s"}, cfg)
print(resp)
```

Permit checks inside document tools:

```31:35:src/ai/tools/documents.py
has_perms = async_to_sync(permit.check)(f"{user_id}", "read", "document")
if not has_perms:
    raise Exception("You do not have permission to do search the documents.")
```

#### Supervisor (multi-agent)

```python
from ai.supervisors import get_supervisor
from langchain_core.runnables import RunnableConfig

cfg = RunnableConfig(configurable={"user_id": 1})
supervisor = get_supervisor()
resp = supervisor.invoke({"messages": "Find a good mystery movie and save a note about it."}, cfg)
print(resp)
```

### Jupyter Notebooks

Open notebooks to explore step-by-step:
- `notebook/6-hello-world-ai-agent.ipynb`
- `notebook/7-memory-ai-agent.ipynb`
- `notebook/8-agent-crud.ipynb`
- `notebook/9-tmdb-api-client.ipynb`
- `notebook/10-movie-discovery-ai-agent.ipynb`
- `notebook/11-multi-agent-supervisor.ipynb`
- `notebook/12-roles-and-permissions.ipynb`

Launch:

```powershell
.\venv\Scripts\Activate.ps1
jupyter lab
```

### Environment and Configuration Notes

- Ollama endpoint can be changed via `OLLAMA_BASE_URL` (default `http://localhost:11434`)
- `PERMIT_API_KEY` is mandatory at import-time for `mypermit/client.py`; without it, the app raises a `ValueError`. You can supply a placeholder during development, but permission checks will fail unless it’s a valid key and policies are configured
- `TMDB_API_KEY` is required to get any results from TMDB tools

### Database

SQLite by default. Change to Postgres by editing `DATABASES` in `core/settings.py`.

```76:81:src/core/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # postgres -> Postgres, Neon, Timescale, Docker Postgres
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Run migrations:

```powershell
cd src
python manage.py migrate
```

### Security and Production

- Replace `SECRET_KEY`, disable `DEBUG`, and set `ALLOWED_HOSTS`
- Configure a proper database and HTTPS
- Ensure Permit.io policies and PDP are properly set for your environment

### Troubleshooting

- Permit client error at startup:
  - Ensure `PERMIT_API_KEY` is set. The client is created at import time in `mypermit/client.py`
- TMDB returns 401 or empty results:
  - Verify `TMDB_API_KEY`
- Ollama connection errors:
  - Ensure Ollama is running and the models are pulled. Update `OLLAMA_BASE_URL` if not using default

### License

Add a license of your choice (e.g., MIT) to a `LICENSE` file if distributing.


