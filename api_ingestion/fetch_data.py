import os
import sys
import json
import time
import requests
from datetime import datetime
from dotenv import load_dotenv

# ───────────────────────────────────────────────
# 🔹 Start timer for monitoring
start_time = time.time()

# 🔹 Add project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from configs.fred_series import series

# 🔹 Load API key
load_dotenv()
fred_api_key = os.getenv("FRED_API_KEY")

# ───────────────────────────────────────────────
# 🔹 Utility: log messages to console and file
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    os.makedirs("logs", exist_ok=True)
    with open("logs/pipeline_log.txt", "a", encoding="utf-8") as logf:
        logf.write(f"[{timestamp}] {message}\n")

# ───────────────────────────────────────────────
# 🔹 Fetch data from FRED API
success, failed = [], []
total_records = 0

for s in series:
    series_id = s["series_id"]
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={fred_api_key}&file_type=json"

    log_message(f"🔍 Fetching data for {series_id}...")

    try:
        # Add retry mechanism for reliability
        for attempt in range(3):
            try:
                response = requests.get(url, timeout=15)
                response.raise_for_status()
                break
            except Exception as e:
                log_message(f"⚠️ Retry {attempt+1}/3 failed for {series_id}: {e}")
                time.sleep(2)
        else:
            log_message(f"❌ All retries failed for {series_id}")
            failed.append(series_id)
            continue

        if response.status_code == 200:
            data = response.json()
            records = len(data.get("observations", []))
            total_records += records

            output_dir = "data/raw"
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"{series_id}_{today}.json"
            filepath = os.path.join(output_dir, filename)

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            log_message(f"✅ Saved {filename} ({records} records)")
            success.append(series_id)
        else:
            log_message(f"❌ Failed to fetch {series_id} (status: {response.status_code})")
            failed.append(series_id)

    except Exception as e:
        log_message(f"❌ Error fetching {series_id}: {e}")
        failed.append(series_id)

# ───────────────────────────────────────────────
# 🔹 Summary
duration = round(time.time() - start_time, 2)
log_message("───────────────────────────────────────────────")
log_message(f"✅ Pipeline completed in {duration}s")
log_message(f"📦 Total records fetched: {total_records}")
log_message(f"🟢 Success: {success}")
log_message(f"🔴 Failed: {failed if failed else 'None'}")
log_message("───────────────────────────────────────────────")
