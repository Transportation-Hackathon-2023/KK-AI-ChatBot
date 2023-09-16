
import logging
from flask import Flask, render_template, request, jsonify
import sqlite3
import spacy
import math
import os
from flask_cors import CORS

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# App version
__version__ = '0.1.5'

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO)
logging.info("Starting the application. Version: {}".format(__version__))

app = Flask(__name__)
CORS(app)

def initialize_database():
    try:
        logging.info("Initializing database")
        conn = sqlite3.connect('transportation.db')
        c = conn.cursor()
        
        # Create table for bus schedules
        c.execute('''
        CREATE TABLE IF NOT EXISTS bus_schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT,
            departure_time TEXT,
            arrival_time TEXT
        )
        ''')
        
        # Create table for fare details
        c.execute('''
        CREATE TABLE IF NOT EXISTS fare_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            route_name TEXT,
            fare_amount REAL
        )
        ''')
        
        # Create table for user queries
        c.execute('''
        CREATE TABLE IF NOT EXISTS user_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query_text TEXT,
            response_text TEXT
        )
        ''')
        
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error("Could not initialize database: {}".format(e))

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route("/")
def index():
    return "Welcome to the transportation chatbot"

@app.route("/test_db")
def test_db():
    return "Database test endpoint"

@app.route("/bus_schedule", methods=['GET'])
def get_bus_schedule():
    # Placeholder code to get bus schedules from the database
    return jsonify({"message": "Bus schedule data"})

@app.route("/fare_details", methods=['GET'])
def get_fare_details():
    # Placeholder code to get fare details from the database
    return jsonify({"message": "Fare details"})

@app.route("/ask", methods=['POST'])
def ask_chatbot():
    # Placeholder code for chatbot interaction
    return jsonify({"message": "Chatbot response"})

if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
