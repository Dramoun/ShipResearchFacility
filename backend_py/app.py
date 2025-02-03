from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins for cross-origin requests

# Dummy data for testing purposes
data = {
    "generation": 1,
    "cells": [
        {"x": 5, "y": 5, "state": 1},
        {"x": 6, "y": 5, "state": 1},
        {"x": 7, "y": 5, "state": 1},
    ]
}

@app.route('/get_data', methods=['GET'])
def get_data():
    # Return current generation data
    return jsonify(data)

@app.route('/update_data', methods=['POST'])
def update_data():
    # Receive data from frontend (React) or other sources
    new_data = request.json
    data.update(new_data)  # Example of updating data with new input
    return jsonify({"message": "Data updated successfully"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Runs the app on port 5000


