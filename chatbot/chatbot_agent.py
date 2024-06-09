import os
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_functions_agent, Tool, AgentExecutor
from langchain import hub

from chatbot.moviedb_cypher_chain import movie_cypher_chain

# Load environment variables from a .env file
from dotenv import load_dotenv
load_dotenv()

# Retrieve the OpenAI model name for the movie agent from environment variables
MOVIE_AGENT_MODEL = os.getenv("MOVIE_AGENT_MODEL")

# Load the prompt template for the agent from the LangChain hub
movie_agent_prompt = hub.pull("hwchase17/openai-functions-agent")

# Define the tools that the agent can use
tools = [
    Tool(
        name="Graph",
        func=movie_cypher_chain.invoke,
        description="""Useful for answering questions about movies,
        actors, directors, release dates, and other movie-related details.
        Use the entire prompt as input to the tool. For instance, if the prompt is
        "Who directed the movie 'Inception'?", the input should be "Who directed the movie 'Inception'?".
        """,
    ),
]

# Initialize the chat model with the specified OpenAI model
chat_model = ChatOpenAI(
    model=MOVIE_AGENT_MODEL,
    temperature=0,
)

# Create the movie retrieval-augmented generation (RAG) agent with the chat model, prompt, and tools
movie_rag_agent = create_openai_functions_agent(
    llm=chat_model,
    prompt=movie_agent_prompt,
    tools=tools,
)

# Create an executor for the movie RAG agent
movie_rag_agent_executor = AgentExecutor(
    agent=movie_rag_agent,
    tools=tools,
    return_intermediate_steps=False,  # Do not return intermediate steps
    verbose=True,  # Enable verbose logging
    return_only_outputs=False,  # Return the full output including metadata
)