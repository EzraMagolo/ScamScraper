Scam Site Scraper

Overview

The Scam Site Scraper is a Python-based web scraping tool that analyzes websites to determine if they are potentially malicious or fraudulent. It integrates with Google's Safe Browsing API and scrapes metadata from websites to provide insights into their legitimacy.

Features

Website Metadata Scraping: Extracts website descriptions, links, and titles.

Google Safe Browsing API Integration: Checks if a website is flagged as dangerous.

Database Storage: Saves results to a MongoDB database.

Flask API: Provides an endpoint for checking website safety.

Technologies Used

Python (Flask, Requests, BeautifulSoup)

Google Safe Browsing API

MongoDB (for data storage)

Flask (for API service)

Setup Instructions

Prerequisites

Ensure you have the following installed:

Python 3.10+

MongoDB (local or cloud instance)

Google Cloud API Key (for Safe Browsing API)

Installation Steps

Clone the Repository

git clone https://github.com/yourusername/scam-site-scraper.git
cd scam-site-scraper

Create a Virtual Environment (Optional but recommended)

python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate

Install Dependencies

pip install -r requirements.txt

Set Up Environment Variables
Create a .env file in the project root and add:

MONGO_URI=mongodb://localhost:27017/scam_scraper
GOOGLE_API_KEY=your_google_api_key

Running the Application

Start the Flask server:

python main.py

By default, it runs on http://127.0.0.1:5000/.

API Usage

Check Website Safety

Endpoint: POST /analyze

Request Body:

{
"url": "https://example.com"
}

Response Example:

{
"url": "https://example.com",
"google_safebrowsing": {
"matches": [
{
"threatType": "MALWARE",
"platformType": "ANY_PLATFORM"
}
]
},
"scraped": {
"title": "Example Website",
"description": "This is an example site.",
"links": ["https://example.com/about"]
}
}

Troubleshooting

Google Safe Browsing API Not Returning Data

Ensure your API key is enabled for Safe Browsing API.

Check for rate limits.

If the website is safe, the response may return an empty {}.

Flask Not Running or API Not Responding

Ensure MongoDB is running (mongod service).

Check for syntax errors in .env file.

Run with python main.py and check logs for errors.

Future Improvements

Add machine learning to improve scam detection accuracy.

Implement frontend dashboard for easier interaction.

Support bulk URL scanning.

License

This project is open-source and available under the MIT License.

Author: Ezra Tunuka Magolo📧 Contact: ezratunuka14@gmail.comGitHub: EzraMagolo
