from langgraph.prebuilt import create_react_agent

from ai.llms import get_local_llm
from ai.tools import (
    document_tools,
    movie_discovery_tools
)

def get_document_agent(model=None, checkpointer=None):
    llm_model = get_local_llm(model or "llama3.1:8b")

    agent = create_react_agent(
        model=llm_model,  
        tools=document_tools,  
        prompt="You are a helpful assistant in managing a user's documents within this app.",
        checkpointer=checkpointer,
        name="document-assistant"
    )
    return agent


def get_movie_discovery_agent(model=None, checkpointer=None):
    llm_model = get_local_llm(model or "llama3.1:8b")

    agent = create_react_agent(
        model=llm_model,  
        tools=movie_discovery_tools,  
        prompt="You are a helpful assistant in finding and discovering information about movies.",
        checkpointer=checkpointer,
         name="movie-discovery-assistant"
    )
    return agent