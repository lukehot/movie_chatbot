# Movie Chatbot

This project is a terminal-based chatbot that queries a Neo4J database to answer questions about movies. The chatbot has memory capabilities and a feedback mechanism.

## Setup

### Prerequisites

- Python 3.x
- Neo4J Database

### Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd movie_chatbot

2. Install the dependencies
   ```bash
   python3 -m venv chatbot_env
   source chatbot_env/bin/activate  # On Windows use `chatbot_env\Scripts\activate`

   pip install -r requirements.txt


3. config .env to include the following
    NEO4J_URI=bolt://3.88.130.123:7687
    NEO4J_USER=neo4j
    NEO4J_PASSWORD=receivers-slice-thirteen
    OPENAI_MODEL_NAME=gpt-3.5-turbo-0125
    MOVIE_AGENT_MODEL=gpt-3.5-turbo-0125
    OPENAI_API_KEY=YOUR_API_KEY

4. python main.py 