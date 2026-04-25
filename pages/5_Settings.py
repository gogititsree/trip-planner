import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from datetime import datetime
from utils import load_config, save_config

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.title("⚙️ Trip Settings")
st.caption("All changes are written to trip_config.json and reflected across the entire app.")

config = load_config()
trip = config["trip"]

with st.form("settings_form"):
    st.subheader("Trip Info")
    col1, col2 = st.columns(2)
    with col1:
        title = st.text_input("Trip Title", value=trip["title"])
        origin = st.text_input("Origin City & Airport Code", value=trip["origin"])
        destination = st.text_input("Destination City & Airport Code", value=trip["destination"])
        travelers = st.number_input("Number of Travelers", min_value=1, max_value=50, value=int(trip["travelers"]))

    with col2:
        departure_date = st.date_input(
            "Departure Date",
            value=datetime.strptime(trip["departure_date"], "%Y-%m-%d").date(),
        )
        return_date = st.date_input(
            "Return Date",
            value=datetime.strptime(trip["return_date"], "%Y-%m-%d").date(),
        )
        currency_home = st.text_input("Home Currency Code (e.g. INR)", value=trip["currency_home"])
        currency_local = st.text_input("Local Currency Code (e.g. IDR)", value=trip["currency_local"])

    st.subheader("Exchange Rate")
    exchange_rate = st.number_input(
        f"1 {trip['currency_home']} = X {trip['currency_local']}",
        min_value=0.01,
        value=float(trip["exchange_rate"]),
        step=1.0,
        format="%.2f",
        help="Update this manually before your trip for accurate budget conversions.",
    )

    st.subheader("Notes")
    notes = st.text_area("Trip Notes", value=trip.get("notes", ""), height=100)

    submitted = st.form_submit_button("💾 Save Settings")

if submitted:
    if return_date <= departure_date:
        st.error("Return date must be after departure date.")
    else:
        config["trip"].update({
            "title": title,
            "origin": origin,
            "destination": destination,
            "travelers": int(travelers),
            "departure_date": str(departure_date),
            "return_date": str(return_date),
            "currency_home": currency_home,
            "currency_local": currency_local,
            "exchange_rate": exchange_rate,
            "notes": notes,
        })
        try:
            save_config(config)
            st.toast("Settings saved!", icon="✅")
            st.rerun()
        except Exception as e:
            st.error(f"Save failed: {e}")
