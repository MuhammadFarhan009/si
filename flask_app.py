from flask import Flask, request, render_template, jsonify
from chatbot_module import read_rules, generate_response

app = Flask(__name__)

# Load rules
rules = read_rules("rules.txt")

@app.route('/')
def chatbot_ui():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = generate_response(user_message.lower(), rules)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
