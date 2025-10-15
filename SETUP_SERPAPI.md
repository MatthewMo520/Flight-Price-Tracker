# SerpAPI Setup Guide

Your flight tracker now uses SerpAPI to get Google Flights data with real booking links!

## Quick Setup (5 minutes)

### 1. Get Your Free SerpAPI Key

1. Go to https://serpapi.com/users/sign_up
2. Sign up for a free account
3. After signing in, go to your dashboard: https://serpapi.com/dashboard
4. Copy your API key

### 2. Add API Key to .env File

Open the `.env` file and replace `YOUR_SERPAPI_KEY_HERE` with your actual API key:

```
SERPAPI_KEY = your_actual_api_key_here
```

### 3. Run Your App

```bash
streamlit run app.py
```

## What Changed?

### Before (Amadeus):
- Generic Google Flights search links
- No direct booking links for specific flights

### After (SerpAPI):
- **Direct booking links** for each specific flight
- Links use Google's `booking_token` to show exact flight with exact price
- When users click "Book Flight", they go straight to the booking page for that flight

## Free Tier Limits

- **100 free searches per month** on the free plan
- Perfect for testing and small projects
- Upgrade available if you need more

## How Booking Links Work

Each flight now includes a `booking_token` from Google Flights. The link format is:
```
https://www.google.com/travel/flights/booking?booking_token={token}
```

This takes users to Google's booking page with:
- The exact flight selected
- The exact price shown
- Options to book through various airlines/OTAs

## Troubleshooting

**Error: "No API key provided"**
- Make sure you added your SerpAPI key to the `.env` file
- Make sure there are no extra quotes around the key

**Error: "No flights found"**
- Check that airport codes are valid (e.g., YYZ, LAX)
- Try different dates (some routes may not be available on certain dates)

**Links not working?**
- The booking tokens are time-sensitive
- Make sure you're clicking fresh search results
- Old tokens may expire after some time

## Support

- SerpAPI Docs: https://serpapi.com/google-flights-api
- Issues with this app? Check the console for error messages
