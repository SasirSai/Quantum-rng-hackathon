from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from helpers.google_sheets_helpers import log_submission

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/ping', methods=['GET'])
def ping():
    """Health check endpoint."""
    return jsonify({"status": "pong"})

@app.route('/submit', methods=['POST'])
def submit_attendance():
    """
    Endpoint to submit attendance.
    Expected JSON payload:
    {
        "roll_no": "student123",
        "ticket": "abc123xyz"
    }
    """
    try:
        data = request.get_json()
        roll_no = data.get('roll_no')
        ticket = data.get('ticket')
        timestamp = datetime.utcnow().isoformat()
        
        if not roll_no or not ticket:
            return jsonify({
                "status": "error",
                "message": "Missing required fields: roll_no and ticket are required"
            }), 400
            
        # Log to Google Sheets
        success = log_submission(roll_no, ticket)
        
        if success:
            return jsonify({
                "status": "success",
                "message": "Attendance recorded successfully",
                "data": {
                    "roll_no": roll_no,
                    "timestamp": timestamp
                }
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to record attendance"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"An error occurred: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
