import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
from utils import load_config, save_config, currency_symbol
from style import apply_styles, section_header

st.set_page_config(page_title="Flights", page_icon="✈️", layout="wide")
apply_styles()
st.title("✈️ Flights")

config = load_config()
sym = currency_symbol(config["trip"]["currency_home"])

COLUMNS = ["id", "leg", "airline", "flight_number", "from", "to", "departure", "arrival", "cost", "notes"]

df = pd.DataFrame(config["flights"]) if config["flights"] else pd.DataFrame(columns=COLUMNS)

st.subheader("Flight Legs")
st.caption("Edit inline, add rows with the + button, delete rows by selecting and pressing Delete.")

edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "id": st.column_config.NumberColumn("ID", disabled=True, width="small"),
        "leg": st.column_config.SelectboxColumn("Leg", options=["Outbound", "Return", "Connecting"], width="small"),
        "airline": st.column_config.TextColumn("Airline"),
        "flight_number": st.column_config.TextColumn("Flight No."),
        "from": st.column_config.TextColumn("From", width="small"),
        "to": st.column_config.TextColumn("To", width="small"),
        "departure": st.column_config.TextColumn("Departure (YYYY-MM-DD HH:MM)"),
        "arrival": st.column_config.TextColumn("Arrival (YYYY-MM-DD HH:MM)"),
        "cost": st.column_config.NumberColumn(f"Cost ({config['trip']['currency_home']})", format="%d"),
        "notes": st.column_config.TextColumn("Notes"),
    },
    hide_index=True,
)

if st.button("💾 Save Flights"):
    records = edited.copy()
    records["cost"] = records["cost"].fillna(0).astype(int)
    for col in ["leg", "airline", "flight_number", "from", "to", "departure", "arrival", "notes"]:
        if col in records.columns:
            records[col] = records[col].fillna("")
    records["id"] = range(1, len(records) + 1)
    config["flights"] = records.to_dict("records")
    save_config(config)
    st.success("Flights saved!")

st.divider()

col1, col2, col3 = st.columns(3)
outbound = df[df["leg"] == "Outbound"]["cost"].sum() if not df.empty else 0
returning = df[df["leg"] == "Return"]["cost"].sum() if not df.empty else 0
total = df["cost"].sum() if not df.empty else 0

col1.metric("Outbound Cost", f"{sym}{outbound:,.0f}")
col2.metric("Return Cost", f"{sym}{returning:,.0f}")
col3.metric("Total Flight Cost", f"{sym}{total:,.0f}")
