"""
Moonlitt Makers - Etsy Store Backend
=====================================
Setup Instructions:
1. Install dependencies:
   pip install flask flask-cors requests python-dotenv

2. Create a .env file in this directory with:
   ETSY_API_KEY=your_etsy_api_key_here
   ETSY_SHOP_ID=your_shop_id_or_name_here

3. Get your Etsy API Key:
   - Go to https://www.etsy.com/developers/register
   - Create an app and copy your "Keystring" (API Key)
   - Your Shop ID is your shop name (e.g., "MoonlittMakers")

4. Run the server:
   python app.py

5. Open index.html in a browser or serve it alongside this backend.
"""

from flask import Flask, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

ETSY_API_KEY = os.getenv("ETSY_API_KEY", "YOUR_ETSY_API_KEY")
ETSY_SHOP_ID = os.getenv("ETSY_SHOP_ID", "YOUR_SHOP_ID")
ETSY_BASE_URL = "https://openapi.etsy.com/v3/application"

HEADERS = {
    "x-api-key": ETSY_API_KEY
}


@app.route("/api/listings")
def get_listings():
    """
    Fetch active listings from your Etsy shop.
    Returns listing title, description, price, images, and Etsy URL.
    """
    try:
        # Step 1: Get active listing IDs from your shop
        shop_url = f"{ETSY_BASE_URL}/shops/{ETSY_SHOP_ID}/listings/active"
        params = {
            "limit": 20,          # Max listings to show
            "offset": 0,
            "includes": ["Images", "MainImage"],
            "fields": "listing_id,title,description,price,url,quantity,state,tags,views"
        }

        response = requests.get(shop_url, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        listings = []
        for item in data.get("results", []):
            # Extract main image
            images = item.get("images", [])
            main_image = item.get("MainImage", {})

            image_url = ""
            if main_image:
                image_url = main_image.get("url_fullxfull", main_image.get("url_570xN", ""))
            elif images:
                image_url = images[0].get("url_fullxfull", images[0].get("url_570xN", ""))

            # Format price
            price_data = item.get("price", {})
            price = f"{price_data.get('currency_code', 'USD')} {float(price_data.get('amount', 0)) / float(price_data.get('divisor', 100)):.2f}"

            # Truncate description for card display
            desc = item.get("description", "")
            short_desc = desc[:200] + "..." if len(desc) > 200 else desc

            listings.append({
                "id": item.get("listing_id"),
                "title": item.get("title", ""),
                "description": short_desc,
                "full_description": desc,
                "price": price,
                "url": item.get("url", f"https://www.etsy.com/shop/{ETSY_SHOP_ID}"),
                "image": image_url,
                "tags": item.get("tags", [])[:5],
                "views": item.get("views", 0)
            })

        return jsonify({
            "success": True,
            "shop_name": "Moonlitt Makers",
            "total": data.get("count", 0),
            "listings": listings
        })

    except requests.exceptions.HTTPError as e:
        return jsonify({
            "success": False,
            "error": f"Etsy API error: {str(e)}",
            "listings": [],
            "demo": True
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "listings": [],
            "demo": True
        }), 500


@app.route("/api/shop")
def get_shop_info():
    """Fetch basic shop info (name, bio, banner)."""
    try:
        url = f"{ETSY_BASE_URL}/shops/{ETSY_SHOP_ID}"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        data = response.json()

        return jsonify({
            "success": True,
            "name": data.get("shop_name", "Moonlitt Makers"),
            "title": data.get("title", ""),
            "announcement": data.get("announcement", ""),
            "icon_url": data.get("icon_url_fullxfull", ""),
            "url": f"https://www.etsy.com/shop/{ETSY_SHOP_ID}"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e),
            "name": "Moonlitt Makers",
            "url": f"https://www.etsy.com/shop/{ETSY_SHOP_ID}"
        })


@app.route("/health")
def health():
    return jsonify({"status": "ok", "shop": ETSY_SHOP_ID})


if __name__ == "__main__":
    print("🌙 Moonlitt Makers Backend Starting...")
    print(f"   Shop ID: {ETSY_SHOP_ID}")
    print(f"   API Key configured: {'Yes' if ETSY_API_KEY != 'YOUR_ETSY_API_KEY' else 'NO - please set in .env'}")
    print("   Server: http://localhost:5000")
    app.run(debug=True, port=5000)
