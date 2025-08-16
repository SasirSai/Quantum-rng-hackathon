import os
import sys
import time
import hashlib
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# Set environment variable directly
os.environ['IBM_QUANTUM_TOKEN'] = 'YOUR_API_TOKEN_HERE'

app = Flask(__name__)
CORS(app)

# Simple test to see if Flask starts
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "pong", "message": "Flask server is running!"})

if __name__ == '__main__':
    print("Starting test Flask server...")
    app.run(host='0.0.0.0', port=5001, debug=True)
