
import logging
from flask import Flask, render_template, request, jsonify
import sqlite3
import spacy
from flask_cors import CORS

# Initialize logging and other configurations
logging.basicConfig(filename='app.log', level=logging.INFO)

# Initialize spaCy NLP model
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)
CORS(app)

def initialize_database():
    conn = sqlite3.connect('transportation.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user_queries (id INTEGER PRIMARY KEY AUTOINCREMENT, query_text TEXT, response_text TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS bus_schedule (id INTEGER PRIMARY KEY AUTOINCREMENT, route_name TEXT, departure_time TEXT, arrival_time TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS fare_details (id INTEGER PRIMARY KEY AUTOINCREMENT, route_name TEXT, fare_amount REAL)")
    conn.commit()
    conn.close()

def simple_chatbot(query):
    doc = nlp(query)
    for token in doc:
        if token.lower_ in ['hello', 'hi', 'hey']:
            return 'Hello! How can I assist you today?'
    return "I'm sorry, I didn't understand that. Could you please rephrase?"

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_query = request.form['query']
        chatbot_response = simple_chatbot(user_query)
        return f'<h1>Your Query:</h1> <p>{user_query}</p> <h1>Chatbot Response:</h1> <p>{chatbot_response}</p>'
    return """    <h1>Welcome to the Transportation Chatbot</h1>
    <form method='post'>
        Query: <input type='text' name='query'>
        <input type='submit'>
    </form>    """

@app.route("/test_db")
def test_db():
    return "Database test endpoint"

@app.route("/bus_schedule", methods=['GET'])
def get_bus_schedule():
    return jsonify({"message": "Bus schedule data"})

@app.route("/fare_details", methods=['GET'])
def get_fare_details():
    return jsonify({"message": "Fare details"})

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
