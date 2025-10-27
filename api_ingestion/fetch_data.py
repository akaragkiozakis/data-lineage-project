import os 
import sys
import json
import requests 
from datetime import datetime, date

# Add project root to Python path to enable imports from configs
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from configs.fred_series import series
from dotenv import load_dotenv
load_dotenv()
fred_api_key = os.getenv("FRED_API_KEY")


def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")



for s in series:
    series_id = s["series_id"]
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id={series_id}&api_key={fred_api_key}&file_type=json"
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            log_message(f"Succeed to fetch {series_id}")
            data = response.json()
            output_dir = "data/raw"
            os.makedirs(output_dir, exist_ok=True)
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"{series_id}_{today}.json"
            filepath = os.path.join(output_dir, filename)


            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            log_message(f"✅ Saved {filename} ({len(data.get('observations', []))} records)")
        else:
            log_message(f"Failed to fetch {series_id}")
    
    except Exception as e:
        log_message(f"❌ Error fetching {series_id}: {e}")

        

