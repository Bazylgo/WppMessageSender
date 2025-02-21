from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os

# Get the current directory (where your Python file is located)
current_directory = os.path.dirname(os.path.realpath(__file__))

# Build the relative path to chromedriver.exe
chrome_driver_path = os.path.join(current_directory, '..', 'chromedriver-win64', 'chromedriver.exe')

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")  # Fix for DevTools error
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--user-data-dir=chrome-data")  # Keeps session logged in

# Load contacts from an Excel/CSV file (Optional)
df = pd.read_csv("../resources/contacts.csv")  # Ensure CSV has 'Phone' column

phone_numbers = df['Phone','Name'].tolist()
names = df['Name'].tolist()

# Start Chrome WebDriver
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open WhatsApp Web
driver.get("https://web.whatsapp.com")

with open('../resources/message.txt', 'r') as file:
    message = file.read().strip()

index = 0

# Loop through phone numbers
for number in phone_numbers:
    message_personalized = f"Hello {names[index]}!\n{message}"
    index += 1
    url = f"https://web.whatsapp.com/send?phone={number}&text={message_personalized}"
    driver.get(url)
    time.sleep(5)  # Wait for chat to load

    try:
        input_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p')

        input_box.send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        print(f"Failed to send message to {number}: {e}")

print("Messages sent successfully!")
driver.quit()