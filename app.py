
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
        logging.info("Initializing database.")
        conn = sqlite3.connect('bus_schedule.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS schedule (route_number INTEGER PRIMARY KEY, departure_time TEXT, arrival_time TEXT, status TEXT)")
        c.execute("INSERT OR IGNORE INTO schedule VALUES (101, '08:00 AM', '09:00 AM', 'On Time')")
        c.execute("INSERT OR IGNORE INTO schedule VALUES (102, '09:00 AM', '10:00 AM', 'Delayed')")
        conn.commit()
        logging.info("Database initialized successfully.")
    except sqlite3.Error as e:
        logging.error("Database error during initialization: {}".format(e))
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

logging.info("Current Working Directory: {}".format(os.getcwd()))

@app.errorhandler(404)
def not_found_error(error):
    logging.warning("404 error encountered.")
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    logging.critical("500 error encountered.")
    return render_template('500.html'), 500

@app.route('/')
def index():
    logging.info("Rendering index page.")
    return render_template('index.html')

@app.route('/test_db')
def test_db():
    try:
        logging.info("Testing database connection.")
        conn = sqlite3.connect('bus_schedule.db')
        c = conn.cursor()
        c.execute("SELECT * FROM schedule LIMIT 5")
        data = c.fetchall()
        logging.info("Fetched data from database: {}".format(data))
        return jsonify(data)
    except sqlite3.Error as e:
        logging.error("Database error in test_db: {}".format(e))
        return jsonify({"error": "Database error"}), 500
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed after test.")

@app.route('/nearest_stop', methods=['POST'])
def nearest_stop():
    logging.info("Processing nearest stop request.")
    user_lat = float(request.json['latitude'])
    user_long = float(request.json['longitude'])
    logging.debug("User latitude: {}, User longitude: {}".format(user_lat, user_long))
    
    # Simulated bus stop locations (latitude, longitude)
    bus_stops = [
        {'name': 'Stop 1', 'latitude': 40.7128, 'longitude': -74.0060},
        {'name': 'Stop 2', 'latitude': 40.7129, 'longitude': -74.0059},
        {'name': 'Stop 3', 'latitude': 40.7130, 'longitude': -74.0061}
    ]
    
    nearest_stop = None
    min_distance = float('inf')
    
    for stop in bus_stops:
        distance = math.sqrt((user_lat - stop['latitude'])**2 + (user_long - stop['longitude'])**2)
        if distance < min_distance:
            min_distance = distance
            nearest_stop = stop['name']
    
    logging.info("Nearest stop determined: {}".format(nearest_stop))
    return jsonify({"response": "The nearest bus stop is {}.".format(nearest_stop)})

@app.route('/plan_trip', methods=['POST'])
def plan_trip():
    logging.info("Processing trip planning request.")
    user_input = request.json['user_input']
    doc = nlp(user_input)
    logging.debug("User input for trip planning: {}".format(user_input))
    
    intent = "unknown"
    
    # Identify intents based on entities and text analysis
    for ent in doc.ents:
        if ent.label_ == "TIME":
            intent = "Ask for schedule"
    
    if intent == "unknown":
        for token in doc:
            if token.lemma_ == "fast":
                intent = "Fastest route"
            elif token.lemma_ == "cheap":
                intent = "Cheapest route"
    
    logging.info("Intent determined: {}".format(intent))
    if intent == "Ask for schedule":
        return jsonify({"response": "The next bus is at X."})
    elif intent == "Fastest route":
        return jsonify({"response": "The fastest route is X."})
    elif intent == "Cheapest route":
        return jsonify({"response": "The cheapest route is Y."})
    else:
        logging.warning("Unknown intent.")
        return jsonify({"response": "I'm sorry, I don't understand your request."})

@app.route('/fare_info', methods=['POST'])
def fare_info():
    logging.info("Processing fare information request.")
    user_input = request.json['user_input']
    logging.debug("User input for fare information: {}".format(user_input))
    
    conn = sqlite3.connect('bus_schedule.db')
    c = conn.cursor()
    
    if "adult" in user_input:
        c.execute("SELECT cost FROM fare_details WHERE fare_type='Adult'")
        fare = c.fetchone()[0]
        logging.info("Fare for adults: {}".format(fare))
        return jsonify({"response": "The fare for adults is ${}".format(fare)})
    elif "student" in user_input:
        c.execute("SELECT cost FROM fare_details WHERE fare_type='Student'")
        fare = c.fetchone()[0]
        logging.info("Fare for students: {}".format(fare))
        return jsonify({"response": "The fare for students is ${}".format(fare)})
    else:
        logging.warning("Unknown fare type.")
        return jsonify({"response": "Please specify the fare type: adult or student."})

if __name__ == '__main__':
    initialize_database()
    logging.info("Starting Flask app.")
    app.run(debug=True)
