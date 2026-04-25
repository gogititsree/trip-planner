import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
WORKSHEETS = ["trip", "flights", "itinerary", "budget", "checklist"]


def _get_spreadsheet(service_account_info, spreadsheet_id):
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client.open_by_key(spreadsheet_id)


def load_from_sheets(service_account_info, spreadsheet_id):
    ss = _get_spreadsheet(service_account_info, spreadsheet_id)

    try:
        trip_ws = ss.worksheet("trip")
    except gspread.WorksheetNotFound:
        raise RuntimeError(
            "Google Sheet not initialised. Run: "
            "python setup_sheets.py --sheet-id YOUR_ID --key-file YOUR_KEY.json"
        )

    # trip: key-value rows
    rows = trip_ws.get_all_values()
    trip_data = {row[0]: row[1] for row in rows[1:] if len(row) >= 2 and row[0]}
    trip_data["travelers"] = int(trip_data.get("travelers", 1))
    trip_data["exchange_rate"] = float(trip_data.get("exchange_rate", 180))

    # flights
    flights = ss.worksheet("flights").get_all_records()
    for f in flights:
        f["cost"] = int(f.get("cost") or 0)
        f["id"] = int(f.get("id") or 0)

    # itinerary: flat rows → nested by day
    itinerary_rows = ss.worksheet("itinerary").get_all_records()
    days_map = {}
    for row in itinerary_rows:
        day_num = int(row.get("day") or 0)
        if not day_num:
            continue
        if day_num not in days_map:
            days_map[day_num] = {
                "day": day_num,
                "date": str(row.get("date", "")),
                "title": str(row.get("day_title", "")),
                "activities": [],
            }
        days_map[day_num]["activities"].append({
            "time": str(row.get("time", "")),
            "title": str(row.get("activity", "")),
            "description": str(row.get("description", "")),
            "cost": int(row.get("cost") or 0),
            "notes": str(row.get("notes", "")),
        })
    itinerary = [days_map[k] for k in sorted(days_map)]

    # budget
    budget_cats = ss.worksheet("budget").get_all_records()
    for b in budget_cats:
        b["estimated"] = int(b.get("estimated") or 0)
        b["actual"] = int(b.get("actual") or 0)

    # checklist: flat rows → nested by category
    checklist = {}
    for row in ss.worksheet("checklist").get_all_records():
        cat = str(row.get("category", "")).strip()
        if not cat:
            continue
        if cat not in checklist:
            checklist[cat] = []
        checked_val = row.get("checked", False)
        checklist[cat].append({
            "item": str(row.get("item", "")),
            "checked": str(checked_val).upper() in ("TRUE", "1", "YES"),
        })

    return {
        "trip": trip_data,
        "flights": flights,
        "itinerary": itinerary,
        "budget": {"categories": budget_cats},
        "checklist": checklist,
    }


def save_to_sheets(config, service_account_info, spreadsheet_id):
    ss = _get_spreadsheet(service_account_info, spreadsheet_id)

    # trip
    ws = ss.worksheet("trip")
    ws.clear()
    ws.update("A1", [["key", "value"]] + [[k, str(v)] for k, v in config["trip"].items()])

    # flights
    ws = ss.worksheet("flights")
    ws.clear()
    headers = ["id", "leg", "airline", "flight_number", "from", "to", "departure", "arrival", "cost", "notes"]
    rows = [[str(f.get(h, "")) for h in headers] for f in config["flights"]]
    ws.update("A1", [headers] + rows)

    # itinerary (flatten)
    ws = ss.worksheet("itinerary")
    ws.clear()
    headers = ["day", "date", "day_title", "time", "activity", "description", "cost", "notes"]
    rows = []
    for day in config["itinerary"]:
        for act in day.get("activities", []):
            rows.append([
                day["day"], day.get("date", ""), day["title"],
                act.get("time", ""), act.get("title", ""), act.get("description", ""),
                act.get("cost", 0), act.get("notes", ""),
            ])
    ws.update("A1", [headers] + rows)

    # budget
    ws = ss.worksheet("budget")
    ws.clear()
    rows = [[c["name"], c["estimated"], c["actual"]] for c in config["budget"]["categories"]]
    ws.update("A1", [["name", "estimated", "actual"]] + rows)

    # checklist
    ws = ss.worksheet("checklist")
    ws.clear()
    rows = []
    for cat, items in config["checklist"].items():
        for item in items:
            rows.append([cat, item["item"], item["checked"]])
    ws.update("A1", [["category", "item", "checked"]] + rows)


def setup_sheets(service_account_info, spreadsheet_id, config):
    """Create worksheet tabs and populate with initial data. Run once."""
    ss = _get_spreadsheet(service_account_info, spreadsheet_id)

    existing = [ws.title for ws in ss.worksheets()]
    for name in WORKSHEETS:
        if name not in existing:
            ss.add_worksheet(title=name, rows=500, cols=20)
            print(f"  Created worksheet: {name}")

    # Remove default Sheet1 now that our sheets exist
    if "Sheet1" in existing:
        try:
            ss.del_worksheet(ss.worksheet("Sheet1"))
            print("  Removed default Sheet1")
        except Exception:
            pass

    save_to_sheets(config, service_account_info, spreadsheet_id)
    print("  Populated all worksheets with trip_config.json data")
