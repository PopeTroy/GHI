import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_metric_engine():
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("CRITICAL ERROR: GROQ_API_KEY missing.")
        return

    client = Groq(api_key=groq_key)

    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate Global SHI and identify the TOP 3 GEOGRAPHIC NODES of systemic collapse.
    EQUATION: (N * P * F * T) / (B * C)
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "health_percent": float,
        "primary_location": "CITY, COUNTRY",
        "risk_nodes": [
            {"loc": "CITY, COUNTRY", "mode": "WAR/RIOT/PROTEST/INFRA", "risk": "HIGH"},
            {"loc": "CITY, COUNTRY", "mode": "WAR/RIOT/PROTEST/INFRA", "risk": "MED"},
            {"loc": "CITY, COUNTRY", "mode": "WAR/RIOT/PROTEST/INFRA", "risk": "MED"}
        ],
        "collapse_time": "string",
        "scroller_feed": "string"
    }
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        raw = json.loads(completion.choices[0].message.content)
        m = raw['metrics']
        
        shi = (m['N'] * m['P'] * m['F'] * m['T']) / (m['B'] * m['C'] if m['B'] * m['C'] != 0 else 0.00001)
        ticker_summary = " | ".join([f"⚠️ {node['loc']} [{node['mode']}]" for node in raw['risk_nodes']])

        output_data = {
            "shi": round(shi, 5),
            "health_percent": raw['health_percent'],
            "location": raw['primary_location'].upper(),
            "collapse_time": raw['collapse_time'].upper(),
            "risk_nodes": raw['risk_nodes'],
            "scroller_feed": f"GLOBAL IMPACT NODES: {ticker_summary} | {raw['scroller_feed'].upper()}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        with open("shi_data.json", "w") as f:
            json.dump(output_data, f, indent=4)
        
        print(f"Engine Sync Success: {output_data['location']}")

    except Exception as e:
        print(f"Logic Engine Failure: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
