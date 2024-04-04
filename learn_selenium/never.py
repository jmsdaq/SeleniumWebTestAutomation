from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

url = "https://google.com"

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get(url)

# Find the search box element
search_box = driver.find_element(By.CLASS_NAME, "gLFyf")

# Enter your search query
search_query = "Lets see how many people get Rick rolled"
search_box.send_keys(search_query)

# Press Enter to perform the search
search_box.send_keys(Keys.RETURN)

# Wait for the search results to load
try:
    search_results = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
    )

    # Find the link with specific text (replace 'Link Text' with the text you want to click)
    link = driver.find_element(By.PARTIAL_LINK_TEXT, "Let's see how many people get Rick rolled")

    # Click on the link
    link.click()

except Exception as e:
    print("An error occurred:", e)

time.sleep(20)

# Close the browser window
driver.quit()