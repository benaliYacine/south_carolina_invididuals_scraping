from selenium import webdriver
import time
import csv
import os


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC





# Set up the path for the webdriver
os.environ['PATH'] += os.pathsep + "C:\\"
    
    # Set up Selenium
driver = webdriver.Chrome()  # It will now recognize the ChromeDriver from the specified directory


# Step 1: Navigate to the URL
driver.get('https://sbs.naic.org/solar-external-lookup/lookup?jurisdiction=SC&searchType=Licensee&entityType=IND')


# Step 2: Wait for the page to load
time.sleep(5)

# Step 3: Click the search button
wait = WebDriverWait(driver, 10)  # Wait for up to 10 seconds
search_button = wait.until(EC.presence_of_element_located((By.ID, 'submitBtn')))

# Scroll down to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Add a short delay to allow any dynamic content to load after scrolling
wait = WebDriverWait(driver, 10)
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
time.sleep(5)
# Scroll down to the bottom of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Add a short delay to allow any dynamic content to load after scrolling
wait = WebDriverWait(driver, 10)
wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
search_button = driver.find_element(By.ID, 'submitBtn')
search_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'submitBtn'))
)
search_button.click()

# Step 4: Wait for the subsequent page to load
time.sleep(10)

# Step 5: Scrape the data from the displayed table

data = []

# Extract table header
wait = WebDriverWait(driver, 500)  # Wait for up to 10 seconds
table = wait.until(EC.presence_of_element_located((By.ID, 'licenseeLookupTable')))
headers = table.find_element(By.TAG_NAME, 'thead').find_elements(By.TAG_NAME, 'th')
data.append([th.text for th in headers])
time.sleep(5)
while True:
    # Extract rows of the table
    table = driver.find_element(By.ID, 'licenseeLookupTable')
    rows = table.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

    # Extracting data for each row
    for row in rows:
        columns = row.find_elements(By.TAG_NAME, 'td')
        rowData = [td.text for td in columns]
        data.append(rowData)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Add a short delay to allow any dynamic content to load after scrolling
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    time.sleep(5)
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Try to click on the "Next" button
    next_buttons = driver.find_elements(By.XPATH, "//ul[@class='pagination justify-content-end']//a[text()='Next']")
    
    # If there's no "Next" button or it's not clickable, break
    if not next_buttons or "disabled" in next_buttons[0].find_element(By.XPATH,"./..").get_attribute("class"):
        break

    next_buttons[0].click()
    time.sleep(5)  # Wait for the next page to load

# Close the driver
driver.quit()

# Save the data to CSV format
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(data)

print("Data saved to 'output.csv'")
