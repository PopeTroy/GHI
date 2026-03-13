import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_metric_engine():
    # Ensure the API Key is present in GitHub Secrets
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("CRITICAL error: GROQ_API_KEY is not configured.")
        return

    client = Groq(api_key=groq_key)

    # The AI logic specifically pinpointing location and mode of systemic failure
    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate SHI and identify the GEOGRAPHIC LOCATION of systemic collapse.
    
    EQUATION: (N * P * F * T) / (B * C)
    
    COLLAPSE MODES: 
    - INFRASTRUCTURAL (Grid/Supply Chain)
    - PROTEST (Domestic Unrest)
    - RIOT (Violent Friction)
    - WAR (Kinetic Conflict)
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "health_percent": float,
        "collapse_type": "INFRASTRUCTURAL | PROTEST | RIOT | WAR",
        "collapse_location": "CITY, COUNTRY (Identify the highest risk node)",
        "collapse_time": "string (e.g., 72 HOURS)",
        "deficiency_alert": "string (The core failure point)",
        "scroller_feed": "string (High-impact summary)"
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
        
        # Calculate the SHI Ratio
        numerator = m['N'] * m['P'] * m['F'] * m['T']
        denominator = m['B'] * m['C']
        shi = numerator / (denominator if denominator != 0 else 0.00001)

        # Structure the payload for the WordPress terminal
        output = {
            "shi": round(shi, 5),
            "health_percent": raw['health_percent'],
            "collapse_type": raw['collapse_type'],
            "location": raw['collapse_location'],
            "collapse_time": raw['collapse_time'],
            "deficiency": raw['deficiency_alert'],
            "scroller_feed": f"📍 IMPACT ZONE: {raw['collapse_location']} | MODE: {raw['collapse_type']} | RISK: {raw['deficiency_alert']} | {raw['scroller_feed']}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        # Write to the JSON file hosted on GitHub Pages
        with open("shi_data.json", "w") as f:
            json.dump(output, f, indent=4)
        
        print(f"GHI Engine Sync Success: {output['location']} - SHI: {output['shi']}")

    except Exception as e:
        print(f"Logic Engine Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
