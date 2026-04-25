#!/usr/bin/env python3
"""
One-time setup: creates worksheet tabs in your Google Sheet and populates
them with data from trip_config.json.

Usage:
    python setup_sheets.py --sheet-id YOUR_SHEET_ID --key-file service_account.json
"""
import argparse
import json
import os
import sys


def main():
    parser = argparse.ArgumentParser(description="Initialise Google Sheets for Trip Planner")
    parser.add_argument("--sheet-id", required=True, help="Google Sheet ID (from its URL)")
    parser.add_argument("--key-file", required=True, help="Path to service account JSON key file")
    args = parser.parse_args()

    if not os.path.exists(args.key_file):
        print(f"Error: key file not found: {args.key_file}")
        sys.exit(1)

    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "trip_config.json")
    with open(config_path, "r") as f:
        config = json.load(f)

    with open(args.key_file, "r") as f:
        service_account_info = json.load(f)

    from sheets_utils import setup_sheets

    print(f"Connecting to sheet: {args.sheet_id}")
    setup_sheets(service_account_info, args.sheet_id, config)

    print("\nDone. Add these to .streamlit/secrets.toml:\n")
    print(f'spreadsheet_id = "{args.sheet_id}"')
    print("\n[gcp_service_account]")
    print("# paste the contents of your service account JSON here as TOML keys")


if __name__ == "__main__":
    main()
