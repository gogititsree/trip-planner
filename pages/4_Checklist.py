import sys
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import streamlit as st
from utils import load_config, save_config

st.set_page_config(page_title="Checklist", page_icon="✅", layout="wide")
st.title("✅ Packing & Documents Checklist")

config = load_config()
checklist = config["checklist"]

all_items = [item for cat in checklist.values() for item in cat]
checked_count = sum(1 for item in all_items if item["checked"])
total = len(all_items)

progress_text = f"{checked_count}/{total} items ready"
st.progress(checked_count / total if total > 0 else 0, text=progress_text)
st.divider()

with st.expander("➕ Add New Category"):
    with st.form("add_cat_form"):
        new_cat = st.text_input("Category Name")
        if st.form_submit_button("Add Category") and new_cat.strip():
            if new_cat.strip() not in config["checklist"]:
                config["checklist"][new_cat.strip()] = []
                save_config(config)
                st.rerun()
            else:
                st.warning("Category already exists.")

changed = False

for cat_name, items in list(checklist.items()):
    cat_checked = sum(1 for i in items if i["checked"])
    with st.expander(f"**{cat_name}** — {cat_checked}/{len(items)}", expanded=True):
        for j, item in enumerate(items):
            col1, col2 = st.columns([8, 1])
            with col1:
                new_val = st.checkbox(item["item"], value=item["checked"], key=f"chk_{cat_name}_{j}")
                if new_val != item["checked"]:
                    config["checklist"][cat_name][j]["checked"] = new_val
                    changed = True
            with col2:
                if st.button("✕", key=f"del_{cat_name}_{j}", help="Remove item"):
                    config["checklist"][cat_name].pop(j)
                    save_config(config)
                    st.rerun()

        with st.form(f"add_item_{cat_name}"):
            col1, col2 = st.columns([4, 1])
            new_item = col1.text_input("New item", key=f"new_input_{cat_name}", label_visibility="collapsed", placeholder="Add item...")
            if col2.form_submit_button("Add") and new_item.strip():
                config["checklist"][cat_name].append({"item": new_item.strip(), "checked": False})
                save_config(config)
                st.rerun()

        if st.button(f"🗑️ Delete '{cat_name}' category", key=f"del_cat_{cat_name}"):
            del config["checklist"][cat_name]
            save_config(config)
            st.rerun()

if changed:
    save_config(config)
    st.rerun()
