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

WebDriverWait(driver, 5).until(
	EC.presence_of_element_located((By.CLASS_NAME, "gLFyf"))
)

input_element = driver.find_element(By.CLASS_NAME, "gLFyf")
input_element.clear()
input_element.send_keys("Let's see how many people get Rick rolled" + Keys.ENTER)

WebDriverWait(driver, 5).until(
	EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "people get Rick rolled"))
)
# Find the link with specific text (replace 'Link Text' with the text you want to click)
link = driver.find_element(By.PARTIAL_LINK_TEXT, "people get Rick rolled")
link.click()

time.sleep(10)

driver.quit()