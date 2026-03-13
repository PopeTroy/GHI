import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_metric_engine():
    # Authentication check
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("CRITICAL: GROQ_API_KEY missing.")
        return

    client = Groq(api_key=groq_key)

    # The AI Logic for Systemic Collapse Diagnostic
    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate SHI and categorize the specific mode of systemic collapse.
    
    EQUATION: (N * P * F * T) / (B * C)
    
    COLLAPSE CATEGORIES:
    - INFRASTRUCTURAL: Grid failure, supply chain snap, digital blackout.
    - PROTEST: Civil unrest, systemic public distrust.
    - RIOT: Violent domestic friction, localized chaos.
    - WAR: Kinetic conflict, geopolitical escalation.
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "health_percent": float,
        "collapse_type": "INFRASTRUCTURAL | PROTEST | RIOT | WAR",
        "collapse_time": "string (e.g. 48 HOURS)",
        "deficiency_alert": "string (The core failure)",
        "scroller_feed": "string (High-impact news bullet)"
    }
    """

    try:
        # Request from Llama 3.3 70B
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        raw = json.loads(completion.choices[0].message.content)
        m = raw['metrics']
        
        # Calculate the Raw SHI Ratio (The Bridge Logic)
        numerator = m['N'] * m['P'] * m['F'] * m['T']
        denominator = m['B'] * m['C']
        shi = numerator / (denominator if denominator != 0 else 0.00001)

        # Build the final dataset for the website
        output = {
            "shi": round(shi, 5),
            "health_percent": raw['health_percent'],
            "collapse_type": raw['collapse_type'],
            "collapse_time": raw['collapse_time'],
            "deficiency": raw['deficiency_alert'],
            "scroller_feed": f"⚠️ COLLAPSE MODE: {raw['collapse_type']} | WINDOW: {raw['collapse_time']} | {raw['scroller_feed']}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        # Save to file for GitHub Pages to host
        with open("shi_data.json", "w") as f:
            json.dump(output, f, indent=4)
        
        print(f"GHI Sync Complete. SHI: {output['shi']} | Health: {output['health_percent']}%")

    except Exception as e:
        print(f"Logic Error: {e}")
        # Prevent Workflow Failure
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
