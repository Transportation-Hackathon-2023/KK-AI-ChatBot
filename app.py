
import logging
import openai
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import sqlite3
import spacy
from flask_cors import CORS

# Initialize logging and other configurations
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize GPT client (Note: Replace the key with your own API key, this is a placeholder)
openai.api_key = "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"

app = Flask(__name__)
CORS(app)

# Initialize Socket.io
socketio = SocketIO(app)

def initialize_database():
    logging.info('Initializing database...')
    # Initialization code for the database

def simple_chatbot(query):
    try:
        logging.info(f"Received query: {query}")
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=query,
            max_tokens=100
        )
        generated_text = response['choices'][0]['text'].strip()
        if generated_text:
            logging.info(f"Generated text: {generated_text}")
            return generated_text
        else:
            logging.warning('Generated text is None or empty.')
            return 'Could not generate a response.'
    except Exception as e:
        logging.error(f"Error in simple_chatbot: {e}")
        return 'An error occurred.'

# Socket.io Event Handlers
@socketio.on('send_message')
def handle_message(msg):
    logging.info(f"Received message: {msg}")
    response = simple_chatbot(msg)
    socketio.emit('receive_message', response)

@app.errorhandler(404)
def not_found_error(error):
    logging.error(f"404 error: {error}")
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error(f"500 error: {error}")
    return jsonify({"error": "Internal server error"}), 500

@app.route("/chat")
def chat():
    return render_template("chat.html")

@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            user_query = request.form['query']
            chatbot_response = simple_chatbot(user_query)
            logging.info(f"Returning chatbot response: {chatbot_response}")
            return f'<h1>Your Query:</h1> <p>{user_query}</p> <h1>Chatbot Response:</h1> <p>{chatbot_response}</p>'
        logging.info("GET request, showing form")
        return """<h1>Welcome to the Transportation Chatbot</h1>
                  <form method='post'>
                      Query: <input type='text' name='query'>
                      <input type='submit'>
                  </form>"""
    except Exception as e:
        logging.error(f"An error occurred in index: {e}")
        return 'An error occurred.'

@app.route("/test_db")
def test_db():
    logging.info("Testing database.")
    return "Database test endpoint"

@app.route("/bus_schedule", methods=['GET'])
def get_bus_schedule():
    logging.info("Fetching bus schedule.")
    return jsonify({"message": "Bus schedule data"})

@app.route("/fare_details", methods=['GET'])
def get_fare_details():
    logging.info("Fetching fare details.")
    return jsonify({"message": "Fare details"})

if __name__ == "__main__":
    initialize_database()
    socketio.run(app, debug=True)
