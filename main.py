import os
import json
import requests
from datetime import datetime
from groq import Groq

def get_vantage_data(api_key):
    # Using Gold (GLD) as a proxy for world economic tension
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GLD&apikey={api_key}"
    try:
        r = requests.get(url).json()
        if "Global Quote" in r:
            return r["Global Quote"]
        return None
    except:
        return None

def run_ghi_diagnostic():
    groq_key = os.getenv('GROQ_API_KEY')
    vantage_key = os.getenv('DEDICATED_KEY')
    
    client = Groq(api_key=groq_key)
    market_data = get_vantage_data(vantage_key)
    
    # YOUR LOGIC: Diagnose world frictions, bottlenecks, and protocols to find the SHI
    prompt = f"""
    AUDIT MISSION: Diagnose the world's current economic frictions, bottlenecks, and filters.
    INPUT DATA: Current Gold Market Data: {json.dumps(market_data)}
    
    1. Identify the primary World Economic Tension.
    2. Identify the Bottlenecks (missing protocols or obstructions).
    3. Identify the Protocols in place to resolve these.
    4. Calculate the SHI (Stability Health Index) based on how much tension is unresolved by protocols.
    
    Return ONLY a JSON object: 
    {{
        "shi": float, 
        "friction": "string", 
        "bottleneck": "string", 
        "protocol": "string"
    }}
    """

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
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

if __name__ == "__main__":
    run_ghi_diagnostic()
