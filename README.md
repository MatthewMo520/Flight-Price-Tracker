# Flight Price Tracker

A full-stack web app that scrapes Kayak.com to find cheap flights.

## Features

- Search real-time flight prices from Kayak
- Results sorted by price (cheapest first)
- Direct booking links to Kayak

## Tech Stack

**Frontend:** React, CSS
**Backend:** Flask, Selenium, BeautifulSoup
**Deployment:** Docker, Render.com

## Project Structure

```
Flight-Price-Tracker/
├── backend/
│   ├── app.py                   
│   ├── requirements.txt
│   └── scrapers/
│       ├── kayak_scraper.py     
│       ├── scraper_utils.py
│       └── multi_scraper.py
├── frontend/
│   ├── src/
│   │   ├── App.js               
│   │   ├── App.css             
│   │   └── index.js
│   ├── public/
│   └── package.json
├── Dockerfile                    
├── render.yaml                   
└── DEPLOYMENT.md                 
```

## To Run Locally:

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Frontend runs on `localhost:3000`, backend on `localhost:5000`.

## To Deploy to Render

1. Push code to GitHub
2. Create Web Service on Render (use Docker)
3. Create Static Site for frontend
4. Set `REACT_APP_API_URL` to your backend URL

Full instructions in [DEPLOYMENT.md](DEPLOYMENT.md).

## How It Works

1. User enters flight info (origin, destination, date)
2. Backend scrapes Kayak.com with Selenium
3. Parses flight data (airline, price, times)
4. Returns sorted results to frontend
5. User clicks "Book Flight" to go to Kayak

## Config Files

**Dockerfile:** Packages Flask backend + Chrome for Selenium into a container
**render.yaml:** Tells Render how to deploy frontend and backend

## Limitations

- Takes 15-20 seconds per search (Selenium is slow)
- May break if Kayak changes their HTML
- Free tier on Render sleeps after 15 min inactivity

## Legal

For educational use. Respect Kayak's terms of service.

## Future Applications

- email system that sends out daily alerts
- scraping more websites (Lots of Captcha so it is hard)
   - can use paid apis to do as well
- include feature for round trips in addition to the one ways
