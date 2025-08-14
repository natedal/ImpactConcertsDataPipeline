# iVoted Data Processing Pipeline

This repository contains scripts to download, process, and upload city-level voting and CVAP (Citizen Voting Age Population) data to Google Sheets.

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- Chrome browser
- Google Cloud Service Account credentials
- Access to Redistricting Data Hub

### Installation
1. Clone this repository
2. Navigate to the project directory:
   ```bash
   cd "iVoted Internship"
   ```
3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
4. Place your Google Cloud service account JSON file in the `code 2/` directory
5. Update the `SPREADSHEET_ID` in `code 2/UploadtoGoogleSheets.py` with your target Google Sheet

## 📁 Project Structure

```
iVoted Internship/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
└── code 2/
    ├── main.py              # Main data processing script
    ├── utility.py           # Data aggregation functions
    ├── UploadtoGoogleSheets.py # Google Sheets upload script
    ├── get_cookies_for_login.py # Cookie management for web scraping
    ├── setup.py             # Automated setup script
    ├── config_example.py    # Example configuration
    ├── files_for_processing/ # Raw downloaded data files
    └── results/             # Processed city-level CSV files
```

## 🔧 Usage

### Step 1: Download and Process City Data

Run the main script to download and process data for all cities:

```bash
cd "code 2"
python main.py
```

**What this does:**
- Downloads voter turnout data from Redistricting Data Hub
- Downloads CVAP data from Redistricting Data Hub  
- Downloads geographic correlation files from MCDC Geocorr
- Processes and aggregates data to city level
- Saves results as CSV files in `results/` directory

**Expected output:**
- Progress messages for each city
- CSV files saved as `{city}.csv` and `{city}_cvap.csv`

### Step 2: Upload to Google Sheets

After processing is complete, upload the results to Google Sheets:

```bash
python UploadtoGoogleSheets.py
```

**What this does:**
- Reads processed CSV files from `results/` directory
- Creates/overwrites worksheets in your Google Sheet
- Combines voting and CVAP data with blank row separator
- Handles API rate limits automatically

## ⚙️ Configuration

### Google Sheets Setup
1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account and download JSON credentials
4. Share your target Google Sheet with the service account email
5. Update `SPREADSHEET_ID` in `code 2/UploadtoGoogleSheets.py`

### File Paths
- **Data processing**: Files are saved to `code 2/results/` directory
- **Upload script**: Reads from `code 2/results/` directory
- **Raw downloads**: Stored in `code 2/files_for_processing/` directory

## 🎯 Cities Currently Processed

The script processes these cities by default:
- Charlotte city, NC
- Asheville city, NC  
- Miami city, FL

To add/remove cities, edit the `cities` list in `code 2/main.py` and `CITY_FILES` in `code 2/UploadtoGoogleSheets.py`.

## 🚨 Troubleshooting

### Common Issues

**Geocorr downloads failing:**
- The script now includes retry logic and better error handling
- Check your internet connection and Redistricting Data Hub access
- Files may take time to generate - the script waits automatically

**Google Sheets API errors:**
- Verify your service account credentials are correct
- Check that the service account has access to your Google Sheet
- The script automatically handles rate limits and retries

**Missing city files:**
- Ensure the city name format matches exactly (e.g., "Charlotte city, NC")
- Check that both `{city}.csv` and `{city}_cvap.csv` exist in `code 2/results/`
- Verify the city is included in both `code 2/main.py` and `code 2/UploadtoGoogleSheets.py`

### Debug Mode
Add print statements or check the console output for detailed progress information. The scripts provide verbose logging of each step.

## 📊 Data Format

### Input Files
- **Voter data**: Block-level turnout and registration statistics
- **CVAP data**: Block-level citizen voting age population by race/ethnicity
- **Geocorr files**: Geographic correlations between blocks and places

### Output Files
- **Voting CSV**: Single column with field names and aggregated values
- **CVAP CSV**: Single column with CVAP field names and aggregated values
- **Google Sheets**: Combined data with blank row separator

## 🔄 Workflow Summary

1. **Setup**: Install dependencies, configure Google credentials
2. **Download**: Run `main.py` to fetch and process all city data
3. **Verify**: Check `results/` directory for generated CSV files
4. **Upload**: Run `UploadtoGoogleSheets.py` to populate Google Sheets
5. **Review**: Verify data appears correctly in your target spreadsheet

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review console output for error messages
3. Verify file paths and permissions
4. Ensure all dependencies are properly installed

## 📝 Notes

- The script includes automatic retry logic for failed downloads
- API rate limits are handled gracefully with waiting periods
- Files are processed sequentially to avoid overwhelming external services
- All intermediate files are preserved for debugging purposes 