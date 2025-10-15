from langgraph_supervisor import create_supervisor

from ai import agents
from ai.llms import get_local_llm


def get_supervisor(model=None, checkpointer=None):
    llm_model = get_local_llm(model or "llama3.1:8b")

    return create_supervisor(
        agents=[
            agents.get_document_agent(),
            agents.get_movie_discovery_agent(),
        ],
        model=llm_model,
        prompt=(
            "You manage a document management assistant and a"
            "movie discovery assistant. Assign work to them."
        ),
    ).compile(checkpointer=checkpointer)