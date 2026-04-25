import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
from utils import load_config, save_config

st.set_page_config(page_title="Itinerary", page_icon="🗓️", layout="wide")
st.title("🗓️ Itinerary")

config = load_config()
days = config["itinerary"]

ACTIVITY_COLUMNS = ["time", "title", "description", "cost", "notes"]

with st.expander("➕ Add New Day"):
    with st.form("add_day_form"):
        col1, col2, col3 = st.columns(3)
        new_day_num = col1.number_input("Day Number", min_value=1, value=len(days) + 1)
        new_day_date = col2.text_input("Date (YYYY-MM-DD)")
        new_day_title = col3.text_input("Title")
        if st.form_submit_button("Add Day"):
            config["itinerary"].append({
                "day": int(new_day_num),
                "date": new_day_date,
                "title": new_day_title,
                "activities": [],
            })
            config["itinerary"].sort(key=lambda d: d["day"])
            save_config(config)
            st.success(f"Day {new_day_num} added!")
            st.rerun()

if not days:
    st.info("No days yet. Add one above.")
else:
    tab_labels = [f"Day {d['day']}: {d['title']}" for d in days]
    tabs = st.tabs(tab_labels)

    for i, tab in enumerate(tabs):
        with tab:
            day = days[i]

            col1, col2, col3 = st.columns([2, 2, 1])
            col1.write(f"**Date:** {day.get('date', 'TBD')}")

            new_title = col2.text_input("Day title", value=day["title"], key=f"title_{i}", label_visibility="collapsed")
            if new_title != day["title"]:
                config["itinerary"][i]["title"] = new_title
                save_config(config)
                st.rerun()

            if col3.button("🗑️ Delete Day", key=f"del_day_{i}"):
                config["itinerary"].pop(i)
                save_config(config)
                st.rerun()

            activities_df = pd.DataFrame(day.get("activities", []))
            if activities_df.empty:
                activities_df = pd.DataFrame(columns=ACTIVITY_COLUMNS)

            edited = st.data_editor(
                activities_df,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "time": st.column_config.TextColumn("Time", width="small"),
                    "title": st.column_config.TextColumn("Activity"),
                    "description": st.column_config.TextColumn("Description"),
                    "cost": st.column_config.NumberColumn("Cost (₹)", format="₹%d", width="small"),
                    "notes": st.column_config.TextColumn("Notes"),
                },
                hide_index=True,
                key=f"activities_{i}",
            )

            col1, col2 = st.columns([1, 4])
            with col1:
                if st.button("💾 Save Day", key=f"save_day_{i}"):
                    records = edited.copy()
                    records["cost"] = records["cost"].fillna(0).astype(int)
                    for col in ["time", "title", "description", "notes"]:
                        if col in records.columns:
                            records[col] = records[col].fillna("")
                    config["itinerary"][i]["activities"] = records.to_dict("records")
                    save_config(config)
                    st.success("Saved!")

            if not edited.empty and "cost" in edited.columns:
                day_total = edited["cost"].fillna(0).sum()
                col2.caption(f"Day total: ₹{day_total:,.0f}")
