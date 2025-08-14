import os
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import time

# 1️⃣  Authorise once with your service‑account credentials ---------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "/Users/natenate/Desktop/iVoted Internship/code 2/totemic-antenna-460818-r8-1446866ce198.json", scope
)
gc = gspread.authorize(creds)

# 2️⃣  Open the master sheet ----------------------------------------------
SPREADSHEET_ID = "1MwaIZj7WTrcLbMxYfh3IfKXzTcEtve0_NxCZdOpuELs"   # <- your ID here
sh = gc.open_by_key(SPREADSHEET_ID)

# 3️⃣  Helper to upload one city ------------------------------------------
def upload_city(city_name: str, voting_csv: str, cvap_csv: str):
    """
    - voting_csv  :  path/to/`<city>.csv`
    - cvap_csv    :  path/to/`<city>_cvap.csv`
    Creates or overwrites a worksheet called <city_name> and
    uploads the voting data (top), a blank row, then the CVAP data.
    """
    # read the two single‑column CSVs exactly as they were written
    voting = pd.read_csv(voting_csv, header=None)   # two columns: [field, value]
    cvap   = pd.read_csv(cvap_csv,   header=None)

    # concat with one blank row between
    combined = pd.concat([voting, cvap], ignore_index=True)

    # create a cleaner worksheet name
    worksheet_name = city_name.split(",")[0].replace(" city", "")  # e.g., "Phoenix" from "Phoenix city, AZ"
    
    # add—or clear & reuse—the worksheet
    try:
        ws = sh.worksheet(worksheet_name)
        sh.del_worksheet(ws)          # start fresh each time
        print(f"Deleted existing worksheet: {worksheet_name}")
    except gspread.WorksheetNotFound:
        pass
    ws = sh.add_worksheet(title=city_name.split(" ")[-1] + "-" + city_name.split(",")[0][:-4],
                          rows=str(len(combined)+10), cols="5")

    # write the dataframe starting at A1 (no headers)
    set_with_dataframe(ws, combined, include_index=False, include_column_header=False)
    print(f"{worksheet_name} uploaded ✔︎")

# 4️⃣  Loop through all your cities ---------------------------------------
CITY_FILES = [
    ("North Carolina","NC","Charlotte city, NC"),    ("North Carolina","NC","Asheville city, NC"),
    ("Florida",   "FL", "Miami city, FL"),
]

for _, _, city in CITY_FILES:
    voting_csv = f"/Users/natenate/Desktop/iVoted Internship/code 2/results/{city}.csv"
    cvap_csv   = f"/Users/natenate/Desktop/iVoted Internship/code 2/results/{city}_cvap.csv"
    print(voting_csv)
    if os.path.exists(voting_csv) and os.path.exists(cvap_csv):
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            try:
                upload_city(city, voting_csv, cvap_csv)
                break  # Success, move to next city
            except gspread.exceptions.APIError as e:
                if "429" in str(e) or "Quota exceeded" in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"⏰ API quota exceeded for {city}. Waiting 60 seconds before retry {retry_count}/{max_retries-1}...")
                        time.sleep(60)
                    else:
                        print(f"❌ Failed to upload {city} after {max_retries} attempts due to quota limits")
                else:
                    print(f"❌ Error uploading {city}: {e}")
                    break  # For non-quota errors, don't retry
            except Exception as e:
                print(f"❌ Unexpected error uploading {city}: {e}")
                break  # For other errors, don't retry
    else:
        print(f"⚠️  Missing files for {city}")
