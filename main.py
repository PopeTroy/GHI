import os
import json
import requests
from datetime import datetime
from groq import Groq

def get_vantage_data(api_key):
    # Using Gold (GLD) as the world tension proxy
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GLD&apikey={api_key}"
    try:
        r = requests.get(url, timeout=10).json()
        if "Global Quote" in r and r["Global Quote"]:
            return r["Global Quote"]
        elif "Note" in r:
            print("Vantage API Alert: Rate limit reached.")
        return {"Note": "Market data unavailable - Using baseline tension"}
    except Exception as e:
        print(f"Connection Error: {e}")
        return None

def run_ghi_diagnostic():
    # Load Secrets
    groq_key = os.getenv('GROQ_API_KEY')
    vantage_key = os.getenv('DEDICATED_KEY')
    
    if not groq_key or not vantage_key:
        print("CRITICAL ERROR: GROQ_API_KEY or DEDICATED_KEY not found in GitHub Secrets.")
        exit(1) # This tells GitHub the run failed if secrets are missing

    market_data = get_vantage_data(vantage_key)
    client = Groq(api_key=groq_key)
    
    # YOUR LOGIC: World tension vs Protocols
    prompt = f"""
    AUDIT MISSION: Diagnose world economic frictions and bottlenecks.
    INPUT: {json.dumps(market_data)}
    1. Identify the primary World Economic Tension.
    2. Identify the Bottlenecks (missing protocols).
    3. Identify the Protocols in place for resolution.
    4. Calculate the SHI (Stability Health Index) 0.0000 - 1.0000.
    Return ONLY JSON: {{"shi": float, "friction": "str", "bottleneck": "str", "protocol": "str"}}
    """

    completion = client.chat.completions.create(
        model="llama3-7b-8192",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    res = json.loads(completion.choices[0].message.content)

    output = {
        "shi": res['shi'],
        "active_problem": res['friction'],
        "bottleneck": res['bottleneck'],
        "protocol": res['protocol'],
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("shi_data.json", "w") as f:
        json.dump(output, f, indent=4)
    print("GHI Sync Successful.")

if __name__ == "__main__":
    run_ghi_diagnostic()
