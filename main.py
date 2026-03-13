import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_metric_engine():
    # Authentication: Ensure GROQ_API_KEY is set in your GitHub Repository Secrets
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("CRITICAL ERROR: GROQ_API_KEY environment variable is missing.")
        return

    client = Groq(api_key=groq_key)

    # Prompt forces the calculation for the world while pinpointing 3 critical nodes
    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate Global SHI and identify the TOP 3 GEOGRAPHIC NODES of systemic collapse.
    
    EQUATION: (N * P * F * T) / (B * C)
    
    COLLAPSE MODES: INFRASTRUCTURAL, PROTEST, RIOT, WAR.
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "health_percent": float,
        "primary_location": "CITY, COUNTRY (Highest Risk Node)",
        "risk_nodes": [
            {"loc": "CITY, COUNTRY", "mode": "WAR/RIOT/PROTEST/INFRA", "risk": "HIGH"},
            {"loc": "CITY, COUNTRY", "mode": "WAR/RIOT/PROTEST/INFRA", "risk": "MED"},
            {"loc": "CITY, COUNTRY", "mode": "WAR/RIOT/PROTEST/INFRA", "risk": "MED"}
        ],
        "collapse_time": "string (e.g., 48 HOURS)",
        "scroller_feed": "string (Systemic news summary)"
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
        
        # Calculate the Raw SHI Ratio
        numerator = m['N'] * m['P'] * m['F'] * m['T']
        denominator = m['B'] * m['C']
        shi_ratio = numerator / (denominator if denominator != 0 else 0.00001)

        # Combine nodes for the ticker
        ticker_summary = " | ".join([f"⚠️ {node['loc']} [{node['mode']}]" for node in raw['risk_nodes']])

        # Final JSON payload structure
        output_data = {
            "shi": round(shi_ratio, 5),
            "health_percent": raw['health_percent'],
            "location": raw['primary_location'].upper(),
            "collapse_time": raw['collapse_time'].upper(),
            "risk_nodes": raw['risk_nodes'],
            "scroller_feed": f"GLOBAL IMPACT NODES: {ticker_summary} | {raw['scroller_feed'].upper()}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        # Save to the static JSON file
        with open("shi_data.json", "w") as f:
            json.dump(output_data, f, indent=4)
        
        print(f"Engine Sync Success: {output_data['location']} Primary | {len(raw['risk_nodes'])} Nodes Tracked")

    except Exception as e:
        print(f"Logic Engine Failure: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
