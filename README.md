# aitinerary

This project is an agentic itinerary recommender for travel lovers.

## Overview

A Python-based Flask web app that collects user travel preferences and filters, then curates a recommended itinerary with sample hotel, car rental, and activity booking suggestions.

## What is included

- `app.py`: Flask application with trip input handling, itinerary builder, save itinerary persistence, and navigation routes
- `templates/base.html`: shared layout with navigation for Home, Saved, Sign in/Sign up, Partners, About Us, Contact Us
- `templates/index.html`: refined trip filter form with flights, hotels, rental car, and intensity fields
- `templates/saved.html`: saved itinerary list and review page
- `templates/signin.html`, `templates/partners.html`, `templates/about.html`, `templates/contact.html`: placeholder pages for the requested subparts
- `static/styles.css`: improved styling for the refined UI
- `requirements.txt`: Flask and OpenAI dependencies

## Run locally

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. (Optional) Set your OpenAI API key to enable AI-based activity recommendations:
   - Windows PowerShell:
     ```powershell
     $env:OPENAI_API_KEY = "your_api_key"
     ```
5. Start the app:
   ```bash
   python app.py
   ```
6. Open `http://127.0.0.1:5000` in your browser.

## Next enhancements

- Add real external API integrations for hotel, car rental, flight, and activity providers
- Extend the UI with more filters from the design document
- Add persistent user sessions and user profile preferences
- Create a booking planner and multi-day itinerary builder
