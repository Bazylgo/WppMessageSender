from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
import os

app = Flask(__name__)

# Get the current directory (where your Python file is located)
current_directory = os.path.dirname(os.path.realpath(__file__))
chrome_driver_path = os.path.join(current_directory, '..', 'chromedriver-win64', 'chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")  # Fix for DevTools error
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--user-data-dir=chrome-data")  # Keeps session logged in

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/send-messages", methods=["POST"])
def send_messages():
    try:
        # Get the uploaded files from the request
        csv_file = request.files["csv"]
        message_text = request.form['message']

        if not csv_file or not message_text:
            return jsonify({"message": "Please upload a CSV file and enter a message!"}), 400

        # Read CSV
        df = pd.read_csv(csv_file)
        phone_numbers = df['Phone'].tolist()
        names = df['Name'].tolist()

        service = Service(chrome_driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Open WhatsApp Web
        driver.get("https://web.whatsapp.com")
        time.sleep(10)  # Wait for WhatsApp Web to load

        # Send messages
        index = 0
        for number in phone_numbers:
            message_personalized = f"Hello {names[index]}!\n {message_text}"
            index += 1
            url = f"https://web.whatsapp.com/send?phone={number}&text={message_personalized}"
            driver.get(url)
            time.sleep(5)  # Wait for chat to load

            try:
                input_box = driver.find_element(By.XPATH,
                                                '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p')
                input_box.send_keys(Keys.RETURN)
                time.sleep(3)
            except Exception as e:
                print(f"Failed to send message to {number}: {e}")

        driver.quit()

        return jsonify({"message": "Messages sent successfully!"})

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)