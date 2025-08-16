import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

def authenticate_google_sheets():
    """
    Authenticate with Google Sheets API using service account credentials.
    
    Returns:
        gspread.Client: Authorized client object or None if authentication fails
    """
    try:
        # Define the scope
        scope = [
            'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive'
        ]
        
        # Path to the credentials file (should be in the parent directory)
        creds_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')
        
        # Authenticate using the service account
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope)
        client = gspread.authorize(creds)
        
        return client
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return None

def log_submission(roll_no, ticket):
    """
    Log attendance submission to Google Sheets.
    
    Args:
        roll_no (str): Student roll number
        ticket (str): Attendance verification ticket
        
    Returns:
        bool: True if logging was successful, False otherwise
    """
    try:
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Authenticate and get the client
        client = authenticate_google_sheets()
        if not client:
            print("Failed to authenticate with Google Sheets API")
            return False
        
        # Open the spreadsheet by title
        sheet = client.open("Quantum Attendance Log").sheet1
        
        # Prepare the new row data
        new_row = [timestamp, str(roll_no), str(ticket)]
        
        # Append the new row to the sheet
        sheet.append_row(new_row)
        
        print(f"Successfully logged attendance for Roll: {roll_no}")
        return True
        
    except gspread.SpreadsheetNotFound:
        print("Error: Could not find 'Quantum Attendance Log' spreadsheet. "
              "Please ensure the sheet exists and is shared with the service account email.")
    except gspread.APIError as e:
        print(f"Google Sheets API Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected error while logging to Google Sheets: {str(e)}")
    
    return False
