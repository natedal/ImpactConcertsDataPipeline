import shutil
import time
import pickle
import zipfile
import os
from utility import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

import pickle
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# # This will download and use the correct ChromeDriver version
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)



## Where to place the csv files from the websites
EXTRACT_DIR = "/Users/natenate/Desktop/iVoted Internship/code 2/files_for_processing"  # Replace with your destination directory

def main_loop(statename, stateabbr, cityname):
    # ## HELPER FUNCTIONS USED IN GETTING CVAP AND TURNOUT DATA
    def unzip_file(zip_file_path, extract_to_dir):
        # Check if the zip file exists
        if not os.path.exists(zip_file_path):
            print(f"The zip file {zip_file_path} does not exist.")
            return

        # Create the target directory if it doesn't exist
        if not os.path.exists(extract_to_dir):
            os.makedirs(extract_to_dir)

        # Open the zip file in read mode
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract all the contents of the zip file into the directory
            zip_ref.extractall(extract_to_dir)
            print(f"Extracted all files to {extract_to_dir}")


    def add_cookies():
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            # Selenium requires 'expiry' in int type, so handle this if needed
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            driver.add_cookie(cookie)


    #############
    # GET TURNOUT DATA
    driver.get("https://redistrictingdatahub.org/dataset/2022-" + STATE_NAME + "-l2-voter-file-elections-turnout-statistics-aggregated-to-2020-census-blocks/")

    time.sleep(1)
    add_cookies()
    time.sleep(2)
    driver.refresh()
    time.sleep(3)

    download_button = driver.find_element(By.CLASS_NAME, value="fa-download")
    download_button.click()
    time.sleep(2)

    agreement = driver.find_element(by="id", value="agreement")
    agreement.click()
    time.sleep(3)
    final_download_button = driver.find_element(by="id", value="thedownloadbutton")
    final_download_button.click()


    time.sleep(5) # Allow file to download.
    zip_file = "/Users/natenate/Downloads/" + STATE_ABBR + "_l2_2022stats_2020block.zip"  # Replace with your zip file path
    unzip_file(zip_file, EXTRACT_DIR)

    time.sleep(2)
    #
    # ########################
    # ## GET CVAP DATA
    driver.get("https://redistrictingdatahub.org/dataset/" + STATE_NAME + "-cvap-data-disaggregated-to-the-2020-block-level-2021/")
    add_cookies()
    time.sleep(2)
    driver.refresh()
    time.sleep(5)

    download_button = driver.find_element(By.CLASS_NAME, value="fa-download")
    download_button.click()
    time.sleep(2)

    agreement = driver.find_element(by="id", value="agreement")
    agreement.click()
    time.sleep(2)
    final_download_button = driver.find_element(by="id", value="thedownloadbutton")
    final_download_button.click()

    time.sleep(10) # Allow file to download.
    zip_file = "/Users/natenate/Downloads/" + STATE_ABBR.lower() + "_cvap_2021_2020_b.zip"  # Replace with your zip file path
    unzip_file(zip_file, EXTRACT_DIR)

    ###############
    ## GET FILE FROM GEOCORR
    driver.get("https://mcdc.missouri.edu/applications/geocorr2022.html")

    select_element = driver.find_element(by="id", value="state")

    select = Select(select_element)
    # Select by visible text
    formatted_state_name = ""
    for word in STATE_NAME.split('-'):
        formatted_state_name += word[0].upper() + word[1:] + " "
    formatted_state_name = formatted_state_name.strip()

    select.select_by_visible_text(formatted_state_name)



    select_element = driver.find_element(By.NAME, "g1_")
    select = Select(select_element)
    select.select_by_value("block")

    select_element = driver.find_element(By.NAME, "g2_")
    select = Select(select_element)
    select.select_by_value("place")

    submit_button = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div/form/div[2]/input[1]")
    submit_button.click()
    print("Submitted geocorr form, waiting for page to process...")
    time.sleep(3)  # Wait longer for form processing

    try:
        download_link = driver.find_element(By.XPATH, "//a[@target='_blank']")
        print("Found download link, starting download...")
        download_link.click()
        
        # Wait longer for file generation and download
        print("Waiting 30 seconds for geocorr file generation and download...")
        time.sleep(5)
    except Exception as e:
        print(f"Error finding or clicking download link: {e}")
        print("Retrying download link search...")
        time.sleep(10)
        try:
            download_link = driver.find_element(By.XPATH, "//a[@target='_blank']")
            download_link.click()
            time.sleep(10)
        except Exception as e2:
            print(f"Failed to download geocorr file after retry: {e2}")
            return  # Exit this city's processing

    # TODO : move geocorr .csv file into files_for_processing

    download_dir = "/Users/natenate/Downloads/"

    # Look specifically for geocorr files (not just any recent file)
    geocorr_files = [f for f in os.listdir(download_dir) if f.startswith("geocorr2022_") and f.endswith(".csv")]
    
    if not geocorr_files:
        print("❌ No geocorr CSV file found in downloads. Download may have failed.")
        return  # Exit this city's processing
    
    # Get the most recent geocorr file
    geocorr_paths = [os.path.join(download_dir, f) for f in geocorr_files]
    recent_file = max(geocorr_paths, key=os.path.getctime)
    recent_file_relative = recent_file.split('/')
    print(f"Found geocorr file: {recent_file_relative[-1]}")
    
    # Verify file is not empty and seems valid
    if os.path.getsize(recent_file) < 100:  # Less than 100 bytes suggests download failed
        print("❌ Geocorr file appears to be empty or corrupted. Download may have failed.")
        return
    
    # Move the most recent file to the destination directory
    shutil.move(recent_file, EXTRACT_DIR)

    print(f"Moved {recent_file} to {EXTRACT_DIR}")
    
    # Wait for file to be fully written and available for processing
    print("Waiting 3 seconds for geocorr file to be fully available...")
    time.sleep(3)

    # Finally,

    voting_file = EXTRACT_DIR + "/" + STATE_ABBR + "_l2_2022stats_2020block.csv"
    corr_file = "/Users/natenate/Desktop/iVoted Internship/code 2/files_for_processing/" + recent_file_relative[4]
    cvap_file = EXTRACT_DIR + "/" + STATE_ABBR.lower() + "_cvap_2021_2020_b.csv"

    agg_voter(voting_file, corr_file, CITY_NAME)
    agg_cvap(cvap_file, corr_file, CITY_NAME)


# Top‑population cities requested (state‑name, state‑abbr, city‑name)
cities = [
    ("florida", "FL", "Jacksonville city, FL"),
    ("florida", "FL", "Miami city, FL"),
    ("north-carolina", "NC", "Raleigh city, NC"),
    ("north-carolina", "NC", "Asheville city, NC"),
    ("north-carolina", "NC", "Durham city, NC"),
    ("south-carolina", "SC", "Columbia city, SC"),
    ("west-virginia", "WV", "Charleston city, WV"),
]

# ---------------------------------------------------------------------
# pass each tuple to your main loop
# ---------------------------------------------------------------------
for STATE_NAME, STATE_ABBR, CITY_NAME in cities:
    try:
        main_loop(STATE_NAME, STATE_ABBR, CITY_NAME)
    except:
        print(STATE_NAME, CITY_NAME)
        continue