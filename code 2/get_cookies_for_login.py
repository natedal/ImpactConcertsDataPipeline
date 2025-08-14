from selenium import webdriver
import pickle
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# This will download and use the correct ChromeDriver version
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)


# Step 2: Open the login page
driver.get('https://redistrictingdatahub.org/login/')  # Replace with the login page URL

# Step 3: Log in manually or using Selenium
time.sleep(20)  # Wait for manual login or adjust this accordingly

# Step 4: Save cookies to a file
pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

# Step 5: Close the browser
driver.quit()
