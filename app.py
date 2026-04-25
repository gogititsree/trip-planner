import streamlit as st
from datetime import date, datetime
import pandas as pd
from utils import load_config

st.set_page_config(page_title="Trip Planner", page_icon="✈️", layout="wide")

config = load_config()
trip = config["trip"]

st.title(f"✈️ {trip['title']}")
st.caption(f"{trip['origin']}  →  {trip['destination']}")
st.divider()

departure = datetime.strptime(trip["departure_date"], "%Y-%m-%d").date()
return_d = datetime.strptime(trip["return_date"], "%Y-%m-%d").date()
today = date.today()
days_left = (departure - today).days
duration = (return_d - departure).days

total_est = sum(c["estimated"] for c in config["budget"]["categories"])
total_act = sum(c["actual"] for c in config["budget"]["categories"])
all_items = [item for cat in config["checklist"].values() for item in cat]
checked_count = sum(1 for item in all_items if item["checked"])

col1, col2, col3, col4 = st.columns(4)

if days_left > 0:
    countdown_label = f"{days_left} days"
elif days_left == 0:
    countdown_label = "Today!"
else:
    countdown_label = "Departed"

col1.metric("Departure In", countdown_label)
col2.metric("Trip Duration", f"{duration} nights")
col3.metric(
    "Budget (INR)",
    f"₹{total_est:,}",
    delta=f"₹{total_act:,} spent" if total_act > 0 else None,
    delta_color="inverse",
)
col4.metric(
    "Checklist",
    f"{checked_count} / {len(all_items)}",
    delta=f"{len(all_items) - checked_count} remaining" if checked_count < len(all_items) else "All done!",
    delta_color="inverse",
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Trip Details")
    details = {
        "From": trip["origin"],
        "To": trip["destination"],
        "Departure": trip["departure_date"],
        "Return": trip["return_date"],
        "Duration": f"{duration} nights",
        "Travelers": str(trip["travelers"]),
        "Exchange Rate": f"1 {trip['currency_home']} = {trip['exchange_rate']} {trip['currency_local']}",
    }
    for k, v in details.items():
        st.write(f"**{k}:** {v}")
    if trip.get("notes"):
        st.info(trip["notes"])

with col2:
    st.subheader("Budget Summary")
    df = pd.DataFrame(config["budget"]["categories"])
    df["remaining"] = df["estimated"] - df["actual"]
    df.columns = ["Category", "Estimated (₹)", "Spent (₹)", "Remaining (₹)"]
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.write(f"**Total Estimated:** ₹{total_est:,}")
    st.write(f"**Total Spent:** ₹{total_act:,}")
    st.write(f"**Remaining:** ₹{total_est - total_act:,}")
