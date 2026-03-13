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

    # UPDATED MODEL & RAW EQUATION LOGIC
    primary_model = "llama-3.3-70b-versatile"
    fallback_model = "llama-3.1-8b-instant"

    prompt = """
    SYSTEM: GHI Quantifiable Equation Engine.
    MISSION: Calculate SHI using the formula: (N * P * F * T) / (B * C).
    REQUIRED VARIABLES: N (Nodes), P (Protocols), F (Filters), T (Time), B (Bottlenecks), C (Corruption).
    Return ONLY JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "friction": "string", "bottleneck": "string", "protocol": "string"
    }
    """

    try:
        try:
            completion = client.chat.completions.create(
                model=primary_model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
        except Exception:
            completion = client.chat.completions.create(
                model=fallback_model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
        
        raw = json.loads(completion.choices[0].message.content)
        m = raw.get('metrics', {})

        # EXTRACT VARIABLES
        N, P, F, T = float(m.get('N', 1)), float(m.get('P', 1)), float(m.get('F', 1)), float(m.get('T', 1))
        B, C = float(m.get('B', 1)), float(m.get('C', 1))
        
        denominator = B * C
        if denominator == 0: denominator = 0.00001
        
        # RAW CALCULATION (REMOVED *100)
        calculated_shi = (N * P * F * T) / denominator

        output = {
            "shi": round(calculated_shi, 5),
            "active_problem": raw.get('friction', 'Scanning...'),
            "bottleneck": raw.get('bottleneck', 'Analyzing...'),
            "protocol": raw.get('protocol', 'Deploying...'),
            "status": "DIMENSIONAL_OVERRIDE_ACTIVE" if calculated_shi < 0.5 else "MEGA_CIRCUIT_ACTIVE",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": {"N": N, "P": P, "F": F, "T": T, "B": B, "C": C}
        }

        with open("shi_data.json", "w") as f:
            json.dump(output, f, indent=4)
        print(f"GHI Engine: Success. Raw SHI: {output['shi']}")

    except Exception as e:
        print(f"Logic Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
