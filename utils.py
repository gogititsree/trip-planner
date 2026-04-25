import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trip_config.json")


def _sheets_credentials():
    """Returns (service_account_info, spreadsheet_id) if Streamlit secrets are configured."""
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets and "spreadsheet_id" in st.secrets:
            return dict(st.secrets["gcp_service_account"]), st.secrets["spreadsheet_id"]
    except Exception:
        pass
    return None, None


def load_config():
    sa_info, sheet_id = _sheets_credentials()
    if sa_info:
        try:
            from sheets_utils import load_from_sheets
            return load_from_sheets(sa_info, sheet_id)
        except Exception as e:
            import streamlit as st
            st.warning(f"⚠️ Google Sheets unavailable ({e}). Showing local data.")
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config):
    sa_info, sheet_id = _sheets_credentials()
    if sa_info:
        from sheets_utils import save_to_sheets
        save_to_sheets(config, sa_info, sheet_id)
    else:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)


def using_sheets():
    sa_info, _ = _sheets_credentials()
    return sa_info is not None


def currency_symbol(code):
    symbols = {"INR": "₹", "USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "AUD": "A$", "CAD": "C$", "SGD": "S$"}
    return symbols.get(code, f"{code} ")
