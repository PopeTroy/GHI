import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_metric_engine():
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("CRITICAL: GROQ_API_KEY missing.")
        return

    client = Groq(api_key=groq_key)

    # QUANTIFIABLE EQUATION METRICS
    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate SHI using the formula: (N * P * F * T) / (B * C).
    
    VARIABLES:
    N = Nodes (Structural Integrity)
    P = Protocols (Procedural Efficiency)
    F = Filters (Sensory Control)
    T = Time/Space (Logistics)
    B = Bottlenecks (Friction)
    C = Corruption (Threats)

    SCAN: Analyze the current world economic/geopolitical state for today's data anchor.
    
    Return ONLY JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "friction": "string",
        "bottleneck": "string",
        "protocol": "string"
    }
    """

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        raw = json.loads(completion.choices[0].message.content)
        m = raw['metrics']

        # RAW FORMULA CALCULATION (No Scaling)
        numerator = m['N'] * m['P'] * m['F'] * m['T']
        denominator = m['B'] * m['C']
        
        # Calculate raw SHI as a decimal ratio
        calculated_shi = (numerator / denominator)

        output = {
            "shi": round(calculated_shi, 5),
            "active_problem": raw['friction'],
            "bottleneck": raw['bottleneck'],
            "protocol": raw['protocol'],
            "status": "DIMENSIONAL_OVERRIDE_ACTIVE" if calculated_shi < 0.5 else "MEGA_CIRCUIT_ACTIVE",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m
        }

        with open("shi_data.json", "w") as f:
            json.dump(output, f, indent=4)
        print(f"GHI Engine: Raw SHI locked at {output['shi']}")

    except Exception as e:
        print(f"Logic Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
