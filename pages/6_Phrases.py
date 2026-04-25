import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
import pandas as pd
from utils import load_config, save_config

st.set_page_config(page_title="Indonesian Phrases", page_icon="🗣️", layout="wide")
st.title("🗣️ Indonesian Phrases")
st.caption("Useful phrases for your trip. Search, browse by category, or add your own.")

config = load_config()
phrases = config.get("phrases", [])

df = pd.DataFrame(phrases) if phrases else pd.DataFrame(columns=["category", "english", "indonesian", "pronunciation"])

# ── Search & filter ──────────────────────────────────────────────
col1, col2 = st.columns([2, 1])
search = col1.text_input("🔍 Search", placeholder="Type any word in English or Indonesian...")
categories = ["All"] + sorted(df["category"].unique().tolist()) if not df.empty else ["All"]
selected_cat = col2.selectbox("Category", categories)

filtered = df.copy()
if selected_cat != "All":
    filtered = filtered[filtered["category"] == selected_cat]
if search:
    mask = (
        filtered["english"].str.contains(search, case=False, na=False) |
        filtered["indonesian"].str.contains(search, case=False, na=False) |
        filtered["pronunciation"].str.contains(search, case=False, na=False)
    )
    filtered = filtered[mask]

st.caption(f"Showing {len(filtered)} of {len(df)} phrases")
st.divider()

# ── Browse by category ───────────────────────────────────────────
if search or selected_cat != "All":
    st.dataframe(
        filtered[["category", "english", "indonesian", "pronunciation"]],
        use_container_width=True,
        hide_index=True,
        column_config={
            "category":      st.column_config.TextColumn("Category", width="small"),
            "english":       st.column_config.TextColumn("English"),
            "indonesian":    st.column_config.TextColumn("Indonesian"),
            "pronunciation": st.column_config.TextColumn("Pronunciation"),
        },
    )
else:
    for cat in sorted(df["category"].unique()):
        cat_df = df[df["category"] == cat][["english", "indonesian", "pronunciation"]]
        with st.expander(f"**{cat}** ({len(cat_df)})", expanded=True):
            st.dataframe(
                cat_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "english":       st.column_config.TextColumn("English"),
                    "indonesian":    st.column_config.TextColumn("Indonesian"),
                    "pronunciation": st.column_config.TextColumn("Pronunciation"),
                },
            )

# ── Edit / Add ───────────────────────────────────────────────────
st.divider()
with st.expander("✏️ Edit phrases / Add your own"):
    st.caption("Add rows, edit cells, delete rows with the row selector. Click Save when done.")
    edited = st.data_editor(
        df,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "category":      st.column_config.SelectboxColumn(
                "Category",
                options=["Greetings", "Basic", "Getting Around", "Food & Eating", "Shopping", "Emergency", "Numbers", "Other"],
            ),
            "english":       st.column_config.TextColumn("English"),
            "indonesian":    st.column_config.TextColumn("Indonesian"),
            "pronunciation": st.column_config.TextColumn("Pronunciation"),
        },
        hide_index=True,
        key="phrases_editor",
    )
    if st.button("💾 Save Phrases"):
        records = edited.fillna("").to_dict("records")
        records = [r for r in records if r.get("english") or r.get("indonesian")]
        config["phrases"] = records
        save_config(config)
        st.toast("Phrases saved!", icon="✅")
        st.rerun()
