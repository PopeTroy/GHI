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

    # System prompt forces specific collapse categories and geographic pinpointing
    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate SHI and identify the GEOGRAPHIC LOCATION of systemic collapse.
    
    EQUATION: (N * P * F * T) / (B * C)
    
    COLLAPSE MODES: 
    - INFRASTRUCTURAL: Grid failure, supply chain collapse, digital blackout.
    - PROTEST: Mass civil unrest, systemic public distrust.
    - RIOT: Violent domestic friction, localized chaos.
    - WAR: Kinetic conflict, geopolitical escalation, border violations.
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {
            "N": float, 
            "P": float, 
            "F": float, 
            "T": float, 
            "B": float, 
            "C": float
        },
        "health_percent": float,
        "collapse_type": "INFRASTRUCTURAL | PROTEST | RIOT | WAR",
        "collapse_location": "CITY, COUNTRY (pinpoint the highest risk node)",
        "collapse_time": "string (e.g., 72 HOURS)",
        "deficiency_alert": "string (The core failure point)",
        "scroller_feed": "string (High-impact news bullet style)"
    }
    """

    try:
        # Generate Diagnostic Data using Llama 3.3 70B
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        raw = json.loads(completion.choices[0].message.content)
        m = raw['metrics']
        
        # Calculate the Raw SHI Ratio (Bridge Logic)
        # Ratio of Protocols (N*P*F*T) over Friction/Bottlenecks (B*C)
        numerator = m['N'] * m['P'] * m['F'] * m['T']
        denominator = m['B'] * m['C']
        shi_ratio = numerator / (denominator if denominator != 0 else 0.00001)

        # Structure final payload for the 1366px HTML Terminal
        output_data = {
            "shi": round(shi_ratio, 5),
            "health_percent": raw['health_percent'],
            "collapse_type": raw['collapse_type'].upper(),
            "location": raw['collapse_location'].upper(),
            "collapse_time": raw['collapse_time'].upper(),
            "deficiency": raw['deficiency_alert'],
            "scroller_feed": f"📍 IMPACT ZONE: {raw['collapse_location'].upper()} | MODE: {raw['collapse_type'].upper()} | {raw['scroller_feed']}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        # Save to shi_data.json (hosted via GitHub Pages)
        with open("shi_data.json", "w") as f:
            json.dump(output_data, f, indent=4)
        
        print(f"Engine Sync Success: {output_data['location']} | SHI: {output_data['shi']}")

    except Exception as e:
        print(f"Logic Engine Execution Failure: {e}")
        # Exit with error code to notify GitHub Actions if it fails
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
