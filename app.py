import streamlit as st
from datetime import date, datetime
import pandas as pd
from utils import load_config, using_sheets, currency_symbol
from style import apply_styles, hero, section_header

st.set_page_config(page_title="Trip Planner", page_icon="✈️", layout="wide")
apply_styles()

with st.sidebar:
    if using_sheets():
        st.caption("📊 Backend: Google Sheets")
        if st.button("🔄 Refresh from Sheets"):
            st.rerun()
    else:
        st.caption("💾 Backend: local JSON")

config = load_config()
trip = config["trip"]

departure = datetime.strptime(trip["departure_date"], "%Y-%m-%d").date()
return_d = datetime.strptime(trip["return_date"], "%Y-%m-%d").date()
today = date.today()
days_left = (departure - today).days
duration = (return_d - departure).days

total_est = sum(c["estimated"] for c in config["budget"]["categories"])
total_act = sum(c["actual"] for c in config["budget"]["categories"])
all_items = [item for cat in config["checklist"].values() for item in cat]
checked_count = sum(1 for item in all_items if item["checked"])
sym = currency_symbol(trip["currency_home"])

if days_left > 0:
    countdown_label = f"✈️ {days_left} days to go"
    metric_label = f"{days_left} days"
elif days_left == 0:
    countdown_label = "✈️ Departing Today!"
    metric_label = "Today!"
else:
    countdown_label = "🌴 Trip in Progress"
    metric_label = "Departed"

travelers = int(trip["travelers"])
hero(
    title=trip["title"],
    route=f"{trip['origin']}  →  {trip['destination']}",
    dates=f"{trip['departure_date']}  –  {trip['return_date']}",
    badge=countdown_label,
    badge_note=f"{duration} nights · {travelers} traveler{'s' if travelers != 1 else ''}",
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Departure In", metric_label)
col2.metric("Trip Duration", f"{duration} nights")
col3.metric(
    f"Budget ({trip['currency_home']})",
    f"{sym}{total_est:,}",
    delta=f"{sym}{total_act:,} spent" if total_act > 0 else None,
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
    section_header("🗺️", "Trip Details")
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
    section_header("💰", "Budget Summary")
    df = pd.DataFrame(config["budget"]["categories"])
    df["remaining"] = df["estimated"] - df["actual"]
    c = trip["currency_home"]
    df.columns = ["Category", f"Estimated ({c})", f"Spent ({c})", f"Remaining ({c})"]
    st.dataframe(df, hide_index=True, use_container_width=True)
    st.write(f"**Total Estimated:** {sym}{total_est:,}")
    st.write(f"**Total Spent:** {sym}{total_act:,}")
    st.write(f"**Remaining:** {sym}{total_est - total_act:,}")
