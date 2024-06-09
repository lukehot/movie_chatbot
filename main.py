import signal
from chatbot.bot import TerminalChatBot


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException


def prompt_for_feedback_with_timer():
    """
    Prompts the user for feedback and assumes 'yes' if no response is received within 5 seconds.
    """
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(5)  # Set the alarm for 5 seconds
    try:
        feedback_input = input("               Was this response helpful? (yes/no): ")
        signal.alarm(0)  # Cancel the alarm
        if feedback_input.lower() == "no":
            print("Bot: I'm sorry. How can I improve?", flush=True)

    except TimeoutException:
        print(" I guess it is ~", flush=True)


def main():
    """
    Main function to run the terminal chatbot.
    """
    bot = TerminalChatBot()

    print("Welcome to the Movie Chatbot!")
    while True:
        user_input = input("You:  ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = bot.get_response(user_input)
        print(f"Bot:  {response}")
        prompt_for_feedback_with_timer()


if __name__ == "__main__":
    main()
