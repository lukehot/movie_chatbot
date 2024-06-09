from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize the Neo4j graph database connection
graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USER"),
    password=os.getenv("NEO4J_PASSWORD"),
)

# Refresh the graph schema
graph.refresh_schema()

# Define the schema template for the graph
schema_template = """
Nodes:
- Movie (title, released)
- Person (name, born)
Relationships:
- [:ACTED_IN] - Person - Movie
- [:DIRECTED] - Person - Movie
- [:REVIEWED] - Person - Movie
- [:PRODUCED] - Person - Movie
- [:WROTE] - Person - Movie
- [:FOLLOWS] - Person - Person
"""

# Define the template for generating Cypher queries
cypher_generation_template = """
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Valid Property Keys:
- born
- data
- id
- name
- nodes
- rating
- relationships
- released
- roles
- style
- summary
- tagline
- title
- visualisation

Valid Node Labels:
- Movie
- Person

Valid Relationship Types:
- ACTED_IN
- DIRECTED
- FOLLOWS
- PRODUCED
- REVIEWED
- WROTE

Examples:

{question}
"""

# Create a prompt template for Cypher query generation
cypher_generation_prompt = PromptTemplate(
    input_variables=["schema", "question"], template=cypher_generation_template
)

# Define the template for generating human-readable responses from Cypher query results
qa_generation_template = """You are an assistant that takes the results
from a Neo4j Cypher query and forms a human-readable response. The
query results section contains the results of a Cypher query that was
generated based on a users natural language question. The provided
information is authoritative, you must never doubt it or try to use
your internal knowledge to correct it. Make the answer sound like a
response to the question.

Previous chat history:

Human: XXX
AI: XXX
Human: XXX
AI: XXX

Query Results:
{context}

Question:
{question}

If the provided information is empty, say you don't know the answer.
Empty information looks like this: []

If the information is not empty, you must review all conversation
history and then provide an answer using the results for the questions.
If the question involves a time duration, assume the query results are
in units of days unless otherwise specified.

Never say you don't have the right information if there is data in
the query results. Make sure to show all the relevant query results
if you're asked.
"""

# Create a prompt template for generating human-readable responses
qa_generation_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template=qa_generation_template,
)

# Initialize the ChatGPT models for generating Cypher queries and QA responses
cypher_llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"), temperature=0)
qa_llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME"), temperature=0)

# Create a GraphCypherQAChain for handling Cypher queries and generating responses
movie_cypher_chain = GraphCypherQAChain.from_llm(
    cypher_llm=cypher_llm,
    qa_llm=qa_llm,
    graph=graph,
    verbose=True,
    qa_prompt=qa_generation_prompt,
    cypher_prompt=cypher_generation_prompt,
    validate_cypher=True,
    top_k=100,
)
