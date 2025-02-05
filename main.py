from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# Initialize Flask App
app = Flask(__name__)

# Connect to MongoDB (Replace with your actual MongoDB connection string)
MONGO_URI = "mongodb+srv://user1:MhASNT1kyrgNLulc@cluster0.vcmjo3v.mongodb.net/"  # Your MongoDB URI here
client = MongoClient(MONGO_URI)
db = client["scam_checker"]
collection = db["scam_sites"]

# Google Safe Browsing API Key (Replace with your actual Google Safe Browsing API Key)
GOOGLE_API_KEY = "AIzaSyCF2_7x6JkSFjTDxgdN7SVjkR_SAW0Jos4"  # Your Google Safe Browsing API Key here

# Function to scrape website data
def scrape_website(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else "No Title"
            meta_desc = soup.find("meta", {"name": "description"})
            description = meta_desc["content"] if meta_desc else "No Description"

            # Extract all links from the website
            links = [a["href"] for a in soup.find_all("a", href=True)]

            return {"url": url, "title": title, "description": description, "links": links}
        else:
            return {"error": "Failed to fetch page"}
    except Exception as e:
        return {"error": str(e)}

# Function to check Google Safe Browsing API
def check_google_safe_browsing(url):
    # Prepare the Safe Browsing API request
    api_url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={GOOGLE_API_KEY}"
    
    request_payload = {
        "client": {
            "clientId": "secret-timing-449912-s5",  # Replace with your custom client ID
            "clientVersion": "1.0."
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }

    # Send the POST request
    response = requests.post(api_url, json=request_payload)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Failed to check Google Safe Browsing API"}

# Flask Route to Analyze a Website
@app.route('/analyze', methods=['POST'])
def analyze_website():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Scrape the website and check it using Google Safe Browsing API
    scraped_data = scrape_website(url)
    google_data = check_google_safe_browsing(url)  # Correct function name

    # Store results in MongoDB
    result = {
        "url": url,
        "scraped": scraped_data,
        "google_safebrowsing": google_data
    }
    
    # Insert result into MongoDB and get the inserted ID
    inserted_result = collection.insert_one(result)
    result["_id"] = str(inserted_result.inserted_id)  # Convert ObjectId to string

    return jsonify(result)



# Flask Route to Get All Scanned Sites
@app.route('/scanned_sites', methods=['GET'])
def get_scanned_sites():
    # Retrieve the sites from the collection
    sites = list(collection.find({}, {"_id": 1}))  # Include _id field in the results

    # Convert ObjectId to string in each site document
    for site in sites:
        site["_id"] = str(site["_id"])  # Convert ObjectId to string

    return jsonify(sites)


# Run Flask App
if __name__ == '__main__':
    app.run(debug=True)
