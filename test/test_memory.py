from chatbot.bot import TerminalChatBot

bot = TerminalChatBot()

user_inputs = [
    "I like Tom Hanks movies ~~~~~ ",
    " what type of movie I like given previous chat?",
    " Who directed the movie 'Cloud Atlas' ", 
]

expected_responses = [
    "Tom Hanks",
    "Tom Hanks",
    "Lilly Wachowski",  
]

for user_input, expected_response in zip(user_inputs, expected_responses):
    print(f"You: {user_input}")

    response = bot.get_response(user_input)
    print(f"Bot: {response}")
    assert (
        expected_response in response
    ), f"Expected '{expected_response}' to be in response"
