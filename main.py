import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_metric_engine():
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key: return

    client = Groq(api_key=groq_key)

    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate SHI and categorize the specific mode of systemic collapse.
    
    EQUATION: (N * P * F * T) / (B * C)
    
    COLLAPSE CATEGORIES:
    - INFRASTRUCTURAL: Grid failure, supply chain snap, digital blackout.
    - PROTEST/RIOT: Civil unrest, systemic public distrust, domestic friction.
    - WAR: Kinetic conflict, border violations, geopolitical escalation.
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "health_percent": float,
        "collapse_type": "INFRASTRUCTURAL | PROTEST | RIOT | WAR",
        "collapse_time": "string",
        "deficiency_alert": "string",
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
        
        # Raw SHI Ratio
        num = m['N'] * m['P'] * m['F'] * m['T']
        den = m['B'] * m['C']
        shi = num / (den if den != 0 else 0.00001)

        output = {
            "shi": round(shi, 5),
            "health_percent": raw['health_percent'],
            "collapse_type": raw['collapse_type'],
            "collapse_time": raw['collapse_time'],
            "deficiency": raw['deficiency_alert'],
            "scroller_feed": f"⚠️ COLLAPSE TYPE: {raw['collapse_type']} | WINDOW: {raw['collapse_time']} | {raw['scroller_feed']}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        with open("shi_data.json", "w") as f:
            json.dump(output, f, indent=4)
    except Exception as e:
        print(f"Logic Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
