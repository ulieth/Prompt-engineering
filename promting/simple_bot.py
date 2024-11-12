import random
import re

class SimpleBot:
    def __init__(self):
        self.responses = {
            r'hi|hello|hey': [
                "Hello! How can I help you today?",
                "Hi there! Nice to meet you!",
                "Hey! What's on your mind?"
            ],
            r'how are you': [
                "I'm doing well, thanks for asking!",
                "I'm great! How are you?",
                "All good here! How about you?"
            ],
            r'bye|goodbye': [
                "Goodbye! Have a great day!",
                "See you later!",
                "Take care!"
            ],
            r'what is your name': [
                "I'm SimpleBot, nice to meet you!",
                "You can call me SimpleBot!",
                "My name is SimpleBot!"
            ],
            r'weather': [
                "I'm not able to check the weather, but I hope it's nice where you are!",
                "Sorry, I don't have access to weather information.",
                "You might want to check a weather app for that information!"
            ]
        }

        # Default response for unknown inputs
        self.default_responses = [
            "I'm not sure how to respond to that.",
            "Could you rephrase that?",
            "I don't understand. Could you try asking something else?"
        ]

    def respond(self, user_input):
        # Convert input to lowercase for better matching
        user_input = user_input.lower()

        # Check each pattern for a match
        for pattern, possible_responses in self.responses.items():
            if re.search(pattern, user_input):
                return random.choice(possible_responses)

        # If no pattern matches, return a default response
        return random.choice(self.default_responses)

def main():
    # Create a bot instance
    bot = SimpleBot()

    print("SimpleBot: Hello! Type 'bye' to exit.")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check for exit condition
        if user_input.lower() == 'bye':
            print("SimpleBot: Goodbye!")
            break

        # Get and print bot's response
        response = bot.respond(user_input)
        print("SimpleBot:", response)

if __name__ == "__main__":
    main()
