from chatbot.chatbot_agent import movie_rag_agent_executor
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import logging

# Set logging level to ERROR to reduce log output
logging.getLogger().setLevel(logging.ERROR)

# Load environment variables from a .env file
load_dotenv()


class TerminalChatBot:
    """A terminal-based chatbot for answering movie-related questions."""

    def __init__(self):
        """Initialize the chatbot with memory and agent."""
        self.memory = ChatMessageHistory(session_id="test-session")

        # Wrap the agent executor with message history handling
        self.agent_with_chat_history = RunnableWithMessageHistory(
            movie_rag_agent_executor,
            # This lambda function provides the memory for a given session ID
            lambda session_id: self.memory,
            input_messages_key="input",  # Key for input messages
            history_messages_key="chat_history",  # Key for chat history messages
        )

    def get_response(self, user_input):
        """
        Get the chatbot's response to a user input.

        Args:
            user_input (str): The user's input message.

        Returns:
            str: The chatbot's response message.
        """
        # Invoke the agent with chat history handling
        response = self.agent_with_chat_history.invoke(
            {"input": user_input},
            config={"configurable": {"session_id": "<foo>"}},
        )
        return response["output"]

    def prompt_for_feedback(self, response):
        """
        Prompt the user for feedback on the chatbot's response.

        Args:
            response (str): The chatbot's response message.

        Returns:
            str: The same response message.
        """
        feedback_input = input("Was this response helpful? (yes/no): ")
        # If the user indicates the response was not helpful, ask for improvement suggestions
        if feedback_input.lower() == "no":
            print("I'm sorry. How can I improve?")
        return response


# Example usage (will be in main.py):
# bot = TerminalChatBot()
