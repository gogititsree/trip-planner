import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
from utils import load_config, save_config, currency_symbol
from style import apply_styles

st.set_page_config(page_title="Budget", page_icon="💰", layout="wide")
apply_styles()
st.title("💰 Budget Tracker")

config = load_config()
trip = config["trip"]
home = trip["currency_home"]
local = trip["currency_local"]
rate = float(trip["exchange_rate"])
sym = currency_symbol(home)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Expense Categories")
    st.caption("Edit estimated and actual spend inline. Add rows for new categories.")

    df = pd.DataFrame(config["budget"]["categories"])

    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "name": st.column_config.TextColumn("Category"),
            "estimated": st.column_config.NumberColumn(f"Estimated ({home})", format="%d"),
            "actual": st.column_config.NumberColumn(f"Spent ({home})", format="%d"),
        },
        hide_index=True,
    )

    if st.button("💾 Save Budget"):
        records = edited.copy()
        records["estimated"] = records["estimated"].fillna(0).astype(int)
        records["actual"] = records["actual"].fillna(0).astype(int)
        records["name"] = records["name"].fillna("Unnamed")
        config["budget"]["categories"] = records.to_dict("records")
        save_config(config)
        st.success("Budget saved!")

    st.divider()

    total_est = edited["estimated"].fillna(0).sum()
    total_act = edited["actual"].fillna(0).sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Estimated", f"{sym}{total_est:,.0f}")
    m2.metric("Total Spent", f"{sym}{total_act:,.0f}")
    m3.metric("Remaining", f"{sym}{total_est - total_act:,.0f}")

with col2:
    st.subheader(f"{home} ↔ {local} Converter")
    st.caption(f"Rate: 1 {home} = {rate:,.0f} {local}")

    direction = st.radio("Direction", [f"{home} → {local}", f"{local} → {home}"])
    amount = st.number_input("Amount", min_value=0.0, value=1000.0, step=100.0)

    if f"{home} →" in direction:
        result = amount * rate
        st.success(f"{sym}{amount:,.0f}  =  {local} {result:,.0f}")
    else:
        result = amount / rate
        st.success(f"{local} {amount:,.0f}  =  {sym}{result:,.2f}")

    st.divider()
    st.subheader("Quick Reference")
    refs = [500, 1000, 2000, 5000, 10000]
    ref_data = pd.DataFrame({
        f"{home}": refs,
        f"{local}": [int(x * rate) for x in refs],
    })
    st.dataframe(ref_data, hide_index=True, use_container_width=True)

st.divider()
st.subheader("Estimated vs Spent")
chart_df = edited[["name", "estimated", "actual"]].fillna(0).set_index("name")
chart_df.columns = [f"Estimated ({home})", f"Spent ({home})"]
st.bar_chart(chart_df)
