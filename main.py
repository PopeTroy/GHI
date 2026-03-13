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

    # MANDATORY EQUATION: (N * P * F * T) / (B * C)
    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate SHI using the formula: (N * P * F * T) / (B * C).
    
    REQUIRED VARIABLES (Return as numbers):
    N = Nodes (Structural Integrity)
    P = Protocols (Procedural Efficiency)
    F = Filters (Sensory Control)
    T = Time/Space (Logistics)
    B = Bottlenecks (Friction)
    C = Corruption (Threats)

    Analyze the current world state to determine these variables.
    
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
        m = raw.get('metrics', {})

        # EXTRACT AND VALIDATE (Ensures no Code 1 crashes)
        N = float(m.get('N', 1))
        P = float(m.get('P', 1))
        F = float(m.get('F', 1))
        T = float(m.get('T', 1))
        B = float(m.get('B', 1))
        C = float(m.get('C', 1))

        # CALCULATION (x100 SCALE)
        denominator = B * C
        if denominator == 0: denominator = 0.00001 # Prevent crash
        
        calculated_shi = ((N * P * F * T) / denominator) * 100

        output = {
            "shi": round(calculated_shi, 5),
            "active_problem": raw.get('friction', 'Scanning...'),
            "bottleneck": raw.get('bottleneck', 'Analyzing...'),
            "protocol": raw.get('protocol', 'Deploying...'),
            "status": "DIMENSIONAL_OVERRIDE_ACTIVE" if calculated_shi < 50.0 else "MEGA_CIRCUIT_ACTIVE",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": {"N": N, "P": P, "F": F, "T": T, "B": B, "C": C}
        }

        with open("shi_data.json", "w") as f:
            json.dump(output, f, indent=4)
        print(f"GHI Engine: SHI Scaled at {output['shi']}")

    except Exception as e:
        print(f"Logic Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
