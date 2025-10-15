from django.conf import settings
from langchain_ollama import ChatOllama, OllamaEmbeddings


def _get_ollama_base_url() -> str:
    """Return the configured Ollama base URL or default local endpoint."""
    # Allow override via Django settings; default to local Ollama
    return getattr(settings, "OLLAMA_BASE_URL", "http://localhost:11434")


def get_local_llm(model: str = "llama3.1:8b", temperature: float = 0):
    """Return a LangChain ChatOllama model configured for local Ollama.

    The default model is llama3.1:8b. Ensure the model is pulled via `ollama pull`.
    """
    return ChatOllama(
        model=model,
        temperature=temperature,
        base_url=_get_ollama_base_url(),
    )


def get_local_embeddings(model: str = "nomic-embed-text"):
    """Return an OllamaEmbeddings instance for local embedding generation."""
    return OllamaEmbeddings(
        model=model,
        base_url=_get_ollama_base_url(),
    )