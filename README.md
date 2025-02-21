
# WhatsApp Message Sender Documentation

## Overview
This Python script uses Selenium WebDriver to send automated WhatsApp messages to a list of contacts. The contacts are loaded from a CSV file that contains phone numbers and names. The script automatically opens WhatsApp Web, navigates to the chat for each contact, and sends a pre-defined message.

## Features
- Uses **Selenium WebDriver** to interact with the Chrome browser.
- Loads contact information from a **CSV file**.
- Sends personalized messages to each phone number listed in the CSV file.
- Keeps the user session logged in through Chrome's user data directory (`--user-data-dir=chrome-data`).
- Handles waiting times to ensure the page elements load properly before performing actions.

## Setup and Installation Guide

### Requirements
1. **Python 3.x** (ensure you have Python installed on your system).
2. **Selenium**: The Python package used for browser automation.
3. **Pandas**: A Python library used to handle CSV file reading.
4. **Chrome WebDriver** (`chromedriver.exe`): The WebDriver for interacting with Google Chrome. It must match your installed version of Google Chrome.
5. **Check Chrome Version**: On your browser, navigate to chrome://settings/help
6. **Install Chrome WebDriver**: Ensure that the binary type is "chromedriver" https://googlechromelabs.github.io/chrome-for-testing/
### Steps to Set Up

1. **Install Python dependencies:**
   First, ensure you have the necessary Python libraries installed. You can use `pip` to install them:
   ```bash
   pip install selenium pandas
   ```

2. **Download ChromeDriver:**
   - Download the **ChromeDriver** that matches your version of Google Chrome from: [ChromeDriver Download](https://googlechromelabs.github.io/chrome-for-testing/).
   - Extract the downloaded folder, and place `chromedriver.exe` in the `chromedriver-win64/` folder in your project.

3. **Set Up Project Structure:**
   Your project directory should be structured as follows:

   ```
   WppMessageSender/
   ├── src/                      # Your Python script folder
   │   └── message_sender.py     # The Python script that sends messages
   ├── chromedriver-win64/        # Folder containing chromedriver.exe
   │   └── chromedriver.exe      # Chromedriver executable
   ├── resources/                # Folder for CSV file
   │   └── contacts.csv          # CSV file with phone numbers and names
   │   └── message.txt           # Text file with the automated message
   ├── requirements.txt          # List of Python dependencies
   └── README.md                 # Documentation
   ```

   Ensure that:
   - `chromedriver.exe` is inside the `chromedriver-win64/` folder.
   - Your contacts CSV file (`contacts.csv`) is inside the `resources/` folder. It should contain at least two columns: **Phone** and **Name**.

4. **Prepare Your Contacts CSV:**
   Create a `contacts.csv` file inside the `resources/` folder with the following structure:

   | Phone       | Name    |
   |-------------|---------|
   | 41774821093 | John    |
   | 41774821094 | Jane    |
   | ...         | ...     |

   The **Phone** column should contain phone numbers in **international format** (e.g., `41774821093` for Switzerland).

## How the Script Works

1. **Set Chrome Options:**
   The script sets several Chrome options to:
   - Disable sandboxing and GPU hardware acceleration.
   - Allow remote debugging.
   - Use a user data directory (`chrome-data`) to retain the login session (so you don’t need to scan the QR code every time).

   ```python
   chrome_options.add_argument("--user-data-dir=chrome-data")  # Keeps session logged in
   ```

2. **Read the Contacts:**
   The script loads the contacts from the `contacts.csv` file using **pandas**. The file is read into a DataFrame, and the script retrieves the phone numbers and names into separate lists.

   ```python
   df = pd.read_csv("resources/contacts.csv")
   phone_numbers = df['Phone'].tolist()
   names = df['Name'].tolist()
   ```

3. **Set Up WebDriver:**
   The WebDriver is set up using the **chromedriver.exe** located in the `chromedriver-win64/` folder. The path to `chromedriver.exe` is dynamically generated relative to the script’s location.

   ```python
   chrome_driver_path = os.path.join(current_directory, '..', 'chromedriver-win64', 'chromedriver.exe')
   ```

4. **Loop Through Contacts and Send Messages:**
   For each phone number in the CSV, the script:
   - Creates a personalized message using the `Name` from the CSV.
   - Constructs the WhatsApp URL with the phone number and message.
   - Opens the URL in the browser and waits for the chat to load.
   - Locates the message input box using XPath and sends the message by pressing **Enter**.

   ```python
   url = f"https://web.whatsapp.com/send?phone={number}&text={message}"
   driver.get(url)
   input_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div[2]/div[1]/p')
   input_box.send_keys(Keys.RETURN)
   ```

5. **Error Handling:**
   If any issue arises while sending the message (e.g., element not found), an error message is printed for that phone number.

## Running the Script

1. **Launch WhatsApp Web:**
   - Before running the script, make sure WhatsApp Web is active, and your account is logged in. The script will use the `chrome-data` directory to retain the session.
   
2. **Run the Script:**
   Run the script from your terminal or PyCharm:

   ```bash
   python src/message_sender.py
   ```

   This will automatically start Chrome, navigate to WhatsApp Web, and begin sending messages to the contacts listed in the CSV file.

## Error Handling and Troubleshooting

- **Unable to find input box**: If the XPath for the message input box changes (due to WhatsApp Web updates), you may need to update the XPath used to locate the input box.
  
- **ChromeDriver Version Mismatch**: Ensure that your **chromedriver.exe** matches the installed version of Google Chrome. If you encounter errors about version mismatches, download the appropriate version of `chromedriver.exe`.

- **Session Issues**: If the script keeps asking for QR code scanning, it might mean that your session is not being saved correctly. Ensure that the `--user-data-dir` argument is correctly set.

## Conclusion

This script is an automated way to send WhatsApp messages from a CSV list of contacts. By using Selenium WebDriver and Chrome, it interacts with WhatsApp Web, making it easy to send bulk messages without manual input. This project can be extended further by adding more features, like error logging, custom message templates, or scheduling.
