# ✈️ Trip Planner

A fully configurable travel planning app built with Python and Streamlit. Plan any trip — flights, day-by-day itinerary, budget tracking, packing checklist — all driven by a single JSON config file.

> Built as a Bali trip planner but reusable for any destination.

## Features

- **Overview** — countdown to departure, budget summary, checklist progress
- **Flights** — add/edit/delete flight legs with cost tracking
- **Itinerary** — day-by-day plan with inline-editable activities per day
- **Budget** — estimated vs actual spend, bar chart, live currency converter
- **Checklist** — packing and documents with categories, checkboxes, and progress bar
- **Settings** — change trip title, dates, cities, currencies, and exchange rate from the UI

All data persists in `trip_config.json` — no database required.

## Setup

**Requirements:** Python 3.8+

```bash
# Clone the repo
git clone https://github.com/your-username/trip-planner.git
cd trip-planner

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Customise for Your Trip

Either edit `trip_config.json` directly, or use the **Settings** page in the app to update:

- Trip title, origin, destination
- Departure and return dates
- Number of travelers
- Home and local currency codes
- Exchange rate

Then fill in your flights, itinerary, budget, and checklist through the UI.

## Project Structure

```
trip-planner/
├── app.py                  # Overview page (home)
├── utils.py                # load_config / save_config helpers
├── trip_config.json        # All trip data (edit this to customise)
├── pages/
│   ├── 1_Flights.py
│   ├── 2_Itinerary.py
│   ├── 3_Budget.py
│   ├── 4_Checklist.py
│   └── 5_Settings.py
└── requirements.txt
```

## Tech Stack

- [Streamlit](https://streamlit.io) — UI framework
- [Pandas](https://pandas.pydata.org) — data tables and charts
- Pure Python — no backend, no database
