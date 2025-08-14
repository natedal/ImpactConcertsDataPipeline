# Example configuration file for iVoted data processing pipeline
# Copy this file to config.py and update with your actual values

# Google Sheets Configuration
SPREADSHEET_ID = "your_google_sheet_id_here"  # Replace with your actual Google Sheet ID

# Service Account Credentials
SERVICE_ACCOUNT_FILE = "your_service_account_credentials.json"  # Replace with your JSON file path

# Processing Configuration
EXTRACT_DIR = "/path/to/your/files_for_processing"  # Directory for raw downloaded files
RESULTS_DIR = "/path/to/your/results"  # Directory for processed CSV files

# Cities to Process (update these as needed)
CITIES = [
    ("north-carolina", "NC", "Charlotte city, NC"),
    ("north-carolina", "NC", "Asheville city, NC"),
    ("florida", "FL", "Miami city, FL"),
    # Add more cities as needed
]

# Wait Times (in seconds) - adjust if needed
FORM_PROCESSING_WAIT = 3
DOWNLOAD_WAIT = 5
FILE_AVAILABILITY_WAIT = 3 