# ✈️ Trip Planner

A fully configurable travel planning app built with Python and Streamlit. Plan any trip — flights, day-by-day itinerary, budget tracking, packing checklist — all driven by a single config file or Google Sheets.

> Built as a Bali trip planner but reusable for any destination.

## Features

- **Overview** — countdown to departure, budget summary, checklist progress
- **Flights** — add/edit/delete flight legs with cost tracking
- **Itinerary** — day-by-day plan with inline-editable activities per day
- **Budget** — estimated vs actual spend, bar chart, live currency converter
- **Checklist** — packing and documents with categories, checkboxes, and progress bar
- **Settings** — change trip title, dates, cities, currencies, and exchange rate from the UI

Supports two backends:
- **Local JSON** (`trip_config.json`) — zero setup, works offline
- **Google Sheets** — private sheet you edit directly; app reads and serves data publicly via Streamlit

## Quick Start (local)

**Requirements:** Python 3.8+

```bash
git clone https://github.com/your-username/trip-planner.git
cd trip-planner
pip install -r requirements.txt
streamlit run app.py
```

## Google Sheets Setup

This gives you a private Google Sheet as the backend. You edit it directly; the public Streamlit app reflects your changes.

### 1. Create a Google Cloud service account

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a project → Enable **Google Sheets API**
3. Go to **IAM & Admin → Service Accounts** → Create service account
4. Create a JSON key and download it (e.g. `service_account.json`)

### 2. Create a Google Sheet and share it with the service account

1. Create a new blank Google Sheet
2. Copy the Sheet ID from the URL: `https://docs.google.com/spreadsheets/d/SHEET_ID_HERE/edit`
3. Share the sheet with your service account email (Editor access)
4. Keep the sheet **private** — the app serves the data, not the sheet itself

### 3. Initialise the sheet

```bash
python setup_sheets.py --sheet-id YOUR_SHEET_ID --key-file service_account.json
```

This creates 5 worksheet tabs and populates them with `trip_config.json` data.

### 4. Configure credentials

```bash
cp .streamlit/secrets.toml.template .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and fill in your `spreadsheet_id` and service account fields.

### 5. Deploy to Streamlit Cloud

1. Push your code to GitHub (secrets.toml is gitignored — never committed)
2. Go to [share.streamlit.io](https://share.streamlit.io), connect your repo, set main file to `app.py`
3. In **App settings → Secrets**, paste the contents of your `secrets.toml`
4. Deploy

The app will now read from your private Google Sheet and serve the data publicly.

## Sheet Structure

| Tab | Contents |
|---|---|
| `trip` | Key-value pairs for trip metadata |
| `flights` | One row per flight leg |
| `itinerary` | Flattened activities (day, date, time, activity, cost…) |
| `budget` | Category, estimated, actual |
| `checklist` | Category, item, checked |

## Project Structure

```
trip-planner/
├── app.py                          # Overview page (home)
├── utils.py                        # load_config / save_config (auto-detects backend)
├── sheets_utils.py                 # Google Sheets read/write logic
├── setup_sheets.py                 # One-time sheet initialisation script
├── trip_config.json                # Local fallback / initial data
├── .streamlit/
│   └── secrets.toml.template       # Credentials template (copy → secrets.toml)
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
- [gspread](https://github.com/burnash/gspread) — Google Sheets API client
- Pure Python — no backend server, no database required
