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
    SYSTEM: GHI Logic Engine - Economic Stability & Growth.
    
    DEFINITIONS:
    - Bottlenecks (B): Deviations from stability (Trade barriers, energy chokepoints, high debt).
    - Protocols (P): Growth improvements (Policy reforms, anti-corruption, innovation).
    - Equation: (N * P * F * T) / (B * C)
    
    MISSION: Identify High Impact Location, 3 Bottleneck Nodes, and 3 Stable (High SHI) Nodes.
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {"N": 1.44, "P": float, "F": float, "T": float, "B": float, "C": float},
        "health_percent": float,
        "primary_high_impact": "CITY, COUNTRY",
        "collapse_type": "HYPER-INFLATION / GRID COLLAPSE / CIVIL UNREST / SUPPLY CHAIN BREAK",
        "collapse_timer": "string (e.g. 72:14:05)",
        "bottleneck_nodes": [{"loc": "CITY, COUNTRY", "deviation": "string"}],
        "high_shi_nodes": [{"loc": "CITY, COUNTRY", "protocol": "string"}],
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

        output_data = {
            "shi": round(shi, 5),
            "health_percent": raw['health_percent'],
            "location": raw['primary_high_impact'].upper(),
            "collapse_type": raw['collapse_type'].upper(),
            "collapse_timer": raw['collapse_timer'],
            "bottlenecks": raw['bottleneck_nodes'],
            "high_shi": raw['high_shi_nodes'],
            "scroller_feed": f"CRITICAL: {raw['primary_high_impact'].upper()} TARGETED FOR {raw['collapse_type'].upper()} | {raw['scroller_feed'].upper()}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        with open("shi_data.json", "w") as f:
            json.dump(output_data, f, indent=4)
        
        print(f"Sync Success: {output_data['location']} - Collapse Type: {output_data['collapse_type']}")

    except Exception as e:
        print(f"Engine Failure: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
