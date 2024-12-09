
import requests
from bs4 import BeautifulSoup
import hashlib
import time

# Configure your Pushover credentials
PUSHOVER_USER_KEY = ''
PUSHOVER_API_TOKEN = ''

# Function to send notification via Pushover
def send_pushover_notification():
    import http.client, urllib
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
    urllib.parse.urlencode({
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": "The FPL site has been updated! Check it out now! https://fantasy.premierleague.com/",
    }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

# URL of the FPL site to monitor
FPL_URL = "https://fantasy.premierleague.com/"

# Function to get the content of the site
def get_site_content(url):
    response = requests.get(url)
    return response.text

# Function to compute hash of the content
def compute_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# Initial content hash
initial_hash = compute_hash(get_site_content(FPL_URL))

while True:
    time.sleep(10)  # Check every 10 seconds

    # Get the current site content and compute its hash
    current_content = get_site_content(FPL_URL)
    current_hash = compute_hash(current_content)

    # Compare the hashes to check for changes
    if current_hash != initial_hash:
        send_pushover_notification()
        initial_hash = current_hash  # Update the initial hash
