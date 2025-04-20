# setup.py
# download the statutes from the internet into a data/raw/statutes folder

import requests
import os

# Define the URL of the statutes
url = "https://www.njleg.state.nj.us/legislative-downloads?downloadType=Statutes"

# Define the path to the data/raw/statutes folder
statutes_path = os.path.join("data", "raw", "statutes")

# Create the data/raw/statutes folder if it doesn't exist
os.makedirs(statutes_path, exist_ok=True)

# Download the statutes
response = requests.get(url)

# Save the statutes to the data/raw/statutes folder
with open(os.path.join(statutes_path, "statutes.txt"), "w") as f:
    f.write(response.text)

print(f"Statutes downloaded and saved to {statutes_path}")

