import time
import hashlib
from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from quantum_generator import generate_quantum_mnemonic
from helpers.google_sheets_helpers import log_submission

# --- Configuration and Initialization ---
import os
try:
    load_dotenv()  # Load environment variables from .env file
    print("Environment variables loaded from .env file")
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")
    # Set environment variable directly as fallback
    os.environ.setdefault('IBM_QUANTUM_TOKEN', 'YOUR_API_TOKEN_HERE')
    print("Using fallback environment configuration")
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for the current attendance code and other state
# This acts as our simple, no-database cache.
current_state = {
    "code": None,
    "minute": None,
    "job_id": None,
    "expires_at": None,
    "submissions_this_minute": set() # To prevent duplicate roll numbers
}

# --- Core Logic ---
def update_mnemonic():
    """
    Scheduled job that runs every 60 seconds to fetch a new quantum code.
    """
    global current_state
    print("⏳ Generating new quantum mnemonic...")

    # Get the current minute since the epoch (a stable identifier for this time window)
    current_minute = int(time.time() / 60)

    # Generate the new code
    result = generate_quantum_mnemonic()

    # Update the global state
    current_state["code"] = result["mnemonic"]
    current_state["minute"] = current_minute
    current_state["job_id"] = result["job_id"]
    current_state["expires_at"] = (current_minute + 1) * 60
    current_state["submissions_this_minute"].clear() # Clear submissions for the new minute
    print(f"🚀 New state set: {current_state}")

def log_to_google_sheet(data):
    """
    Placeholder function for logging attendance data.
    Teammate C will replace this with the actual gspread implementation.
    """
    print(f"LOGGING TO SPREADSHEET (mock): {data}")
    return True # Assume success for now

# --- API Endpoints ---
@app.route('/ping', methods=['GET'])
def ping():
    """A simple endpoint to check if the server is running."""
    return jsonify({"status": "pong"})

@app.route('/current')
def get_current_code():
    """
    Endpoint for the frontend to fetch the current attendance code.
    """
    if not current_state["code"]:
        return jsonify({"error": "Mnemonic not generated yet. Please wait."}), 503

    return jsonify({
        "code": current_state["code"],
        "minute": current_state["minute"],
        "job_id": current_state["job_id"],
        "expires_at": current_state["expires_at"] # For the countdown timer on frontend
    })

@app.route('/submit', methods=['POST'])
def submit_attendance():
    """
    Endpoint for students to submit their attendance ticket.
    """
    data = request.get_json()
    if not data or 'roll' not in data or 'ticket' not in data:
        return jsonify({"status": "error", "message": "Missing 'roll' or 'ticket'."}), 400

    roll_no = data['roll'].strip().upper()
    submitted_ticket = data['ticket'].strip().upper()

    # 1. Prevent duplicate submissions for the same roll number in the same minute
    if roll_no in current_state["submissions_this_minute"]:
        return jsonify({"status": "error", "message": "Already marked for this minute."}), 409 # 409 Conflict

    # 2. Recompute the expected ticket on the server side to verify
    # This prevents tampering on the client side.
    string_to_hash = f"{current_state['code']}{roll_no}{current_state['minute']}"
    expected_ticket = hashlib.sha256(string_to_hash.encode()).hexdigest().upper()[:9]

    # 3. Compare and process
    if submitted_ticket == expected_ticket:
        # On success, log the data and mark this roll as submitted
        log_data = {
            "timestamp": time.time(),
            "roll": roll_no,
            "ticket": submitted_ticket,
            "mnemonic_hash": hashlib.sha256(current_state['code'].encode()).hexdigest(),
            "ip": request.remote_addr
        }
        log_to_google_sheet(log_data)
        current_state["submissions_this_minute"].add(roll_no)

        return jsonify({"status": "success", "message": "Attendance marked."})
    else:
        # On failure, reject the request
        return jsonify({"status": "error", "message": "Invalid ticket."}), 400

# --- App Startup ---
if __name__ == '__main__':
    # Initialize and run the scheduler
    scheduler = BackgroundScheduler()
    # Run the job immediately once, then every 60 seconds
    scheduler.add_job(update_mnemonic, 'interval', seconds=60, id='quantum_job')
    scheduler.start()

    # Run the initial mnemonic generation right away without waiting 60s
    update_mnemonic()

    # Start the Flask server
    app.run(host='0.0.0.0', port=5001, debug=True)
