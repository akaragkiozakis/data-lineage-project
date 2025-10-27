import snowflake.connector
import os
import sys
import json     
from dotenv import load_dotenv

# Add project root to Python path to enable imports from configs
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from configs.fred_series import series
load_dotenv()


account = os.getenv('SNOWFLAKE_ACCOUNT')
user = os.getenv('SNOWFLAKE_USER')
pw = os.getenv('SNOWFLAKE_PASSWORD')
wh = os.getenv('SNOWFLAKE_WAREHOUSE')
db = os.getenv('SNOWFLAKE_DATABASE')
schema = os.getenv('SNOWFLAKE_SCHEMA')
print(account, user, wh, db, schema)

if not all([account, user, wh, db, schema]):
    print("⚠️ Missing one or more Snowflake environment variables.")
    



try:
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=pw,
        warehouse=wh,
        database=db,
        schema=schema
    )
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_VERSION()")
    version = cursor.fetchone()
    print(f"✅ Connected to Snowflake (version: {version[0]})")

    
    print("🧱 Creating table RAW.FRED_DATA if it does not exist...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS RAW.FRED_DATA (
        SERIES_ID STRING,
        INDICATOR_NAME STRING,
        REALTIME_START DATE,
        REALTIME_END DATE,
        OBSERVATION_DATE DATE,
        VALUE FLOAT,
        FILE_LOAD_DATE DATE DEFAULT CURRENT_DATE()
    );
    """)
except Exception as e:
    print(f"Failed to connect and create table in Snowflake {e}")

    


try:    
    raw_dir = "data/raw"
    files = [f for f in os.listdir(raw_dir) if f.endswith(".json")]

    if not files:
        print("⚠️ No JSON files found in data/raw/.")
    else:
            for file in files:
                filepath = os.path.join(raw_dir, file)
                series_id = file.split("_")[0]
                indicator_name = next((s["indicator"] for s in series if s["series_id"] == series_id), None)

                # --- Load JSON data ---
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

                observations = data.get("observations", [])
                if not observations:
                    print(f"⚠️ No observations found in {file}")
                    continue

                # --- Insert rows ---
                insert_query = """
                    INSERT INTO RAW.FRED_DATA 
                    (SERIES_ID, INDICATOR_NAME, REALTIME_START, REALTIME_END, OBSERVATION_DATE, VALUE)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """

                inserted_rows = 0
                for obs in observations:
                    try:
                        cursor.execute(
                            insert_query,
                            (
                                series_id,
                                indicator_name,
                                obs.get("realtime_start"),
                                obs.get("realtime_end"),
                                obs.get("date"),
                                float(obs.get("value")) if obs.get("value") not in ("", None, ".") else None
                            )
                        )
                        inserted_rows += 1
                    except Exception as e:
                        print(f"❌ Error inserting row for {series_id}: {e}")

                conn.commit()
                print(f"✅ Inserted {inserted_rows} rows from {file} into RAW.FRED_DATA")

except Exception as e:
    print(f"❌ Failed to connect or load data: {e}")

finally:
    try:
        cursor.close()
        conn.close()
        print("🔒 Connection closed successfully.")
    except:
        pass