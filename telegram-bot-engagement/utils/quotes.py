import random

def get_relevant_quote_or_joke(topic):
    jokes = [
        f"Why did the AI go to school? To improve its neural network! 🤖",
        f"Quote: 'The future belongs to those who prepare for it today.' – Malcolm X",
        f"Here's one: Learning never exhausts the mind. – Leonardo da Vinci",
        f"Just a joke: Why did the computer get cold? It left its Windows open! 😄"
    ]
    return random.choice(jokes)
