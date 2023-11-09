from flask import Flask, request, render_template, jsonify
import random
import difflib

# Function to read the rules from a text file
def read_rules(file_path):
    rules = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, *responses = line.strip().split(':')
            key = key.strip('"')
            rules[key.lower()] = [response.strip('"') for response in responses]
    return rules


# Function to generate a response based on the user's input
def generate_response(user_input, rules):
    user_words = user_input.split()
    for key in rules:
        key_words = key.split()
        if all(word in user_words for word in key_words):
            return ' '.join(rules[key]).replace('"', '').replace(',', '').replace('  ', ' ')

    similar_query = difflib.get_close_matches(user_input, rules.keys(), n=1)
    if similar_query:
        return ' '.join(rules[similar_query[0]]).replace('"', '').replace(',', '').replace('  ', ' ')
    
        
    return "I'm sorry, I don't understand."
    

# Main loop to interact with the user
def chatbot(file_path):
    rules = read_rules(file_path)
    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('templates/index.html')

    @app.route('/chatbot', methods=['POST'])
    def chatbot():
        user_input = request.form['user_input']
        response = generate_response(user_input.lower(), rules)
        return response

    if __name__ == '__main__':
        app.run()

# Run the chatbot
chatbot("rules.txt")
