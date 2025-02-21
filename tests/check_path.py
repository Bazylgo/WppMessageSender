import os

# Get the current directory (where your Python file is located)
current_directory = os.path.dirname(os.path.realpath(__file__))

# Build the relative path to chromedriver.exe
chrome_driver_path = os.path.join(current_directory, '..', 'chromedriver-win64', 'chromedriver.exe')