# 🌙 Moonlitt Makers — Website Setup Guide

## Files in this project
```
moonlitt-makers/
├── index.html      ← Your website (open this in a browser)
├── app.py          ← Python backend (fetches Etsy listings)
├── requirements.txt
└── README.md       ← This file
```

---

## Step 1 — Get your Etsy API Key

1. Go to → https://www.etsy.com/developers/register
2. Sign in with your Etsy account
3. Create a new app (name it anything, e.g. "Moonlitt Makers Website")
4. Copy the **Keystring** — that's your API key

---

## Step 2 — Find your Shop ID

Your Shop ID is simply your shop name as it appears in your Etsy URL.
For example: `https://www.etsy.com/shop/MoonlittMakers` → Shop ID = `MoonlittMakers`

---

## Step 3 — Configure the backend

Create a file called `.env` in this folder with:

```
ETSY_API_KEY=your_etsy_keystring_here
ETSY_SHOP_ID=MoonlittMakers
```

---

## Step 4 — Install Python dependencies

```bash
pip install flask flask-cors requests python-dotenv
```

---

## Step 5 — Run the backend

```bash
python app.py
```

You should see:
```
🌙 Moonlitt Makers Backend Starting...
   Shop ID: MoonlittMakers
   API Key configured: Yes
   Server: http://localhost:5000
```

---

## Step 6 — Open your website

Just open `index.html` in your browser (double-click it).

The website will automatically call your Python backend and display your Etsy listings live!

---

## How it works — automatic updates

- Whenever you **add a new listing** to Etsy, it will appear on your website automatically on the next page refresh — no manual update needed!
- The website fetches listings fresh from Etsy every time someone opens the page.

---

## Deploying online (optional)

To host this publicly:
- **Backend**: Deploy `app.py` to [Railway](https://railway.app), [Render](https://render.com), or any Python host
- **Frontend**: Host `index.html` on [Netlify](https://netlify.com) or [GitHub Pages]
- Update the `API_URL` in `index.html` to your deployed backend URL

---

## Updating the Etsy shop URL in the website

Open `index.html` and find this line near the bottom:
```js
const ETSY_SHOP_URL = "https://www.etsy.com/shop/MoonlittMakers";
```
Replace `MoonlittMakers` with your actual shop name.
