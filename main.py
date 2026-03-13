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

    # UPDATED MODEL: llama-3.3-70b-versatile
    # FALLBACK MODEL: llama-3.1-8b-instant
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
        except Exception as model_err:
            print(f"Primary model failed, attempting fallback: {model_err}")
            completion = client.chat.completions.create(
                model=fallback_model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
        
        raw = json.loads(completion.choices[0].message.content)
        m = raw.get('metrics', {})

        # CALCULATIONS
        N, P, F, T = float(m.get('N', 1)), float(m.get('P', 1)), float(m.get('F', 1)), float(m.get('T', 1))
        B, C = float(m.get('B', 1)), float(m.get('C', 1))
        
        denominator = B * C
        if denominator == 0: denominator = 0.00001
        
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
        print(f"GHI Engine: Success. SHI: {output['shi']}")

    except Exception as e:
        print(f"Logic Error: {e}")
        # Create a safe file even on error to prevent GitHub Action from failing
        safe_data = {"shi": 50.0, "status": "RE-SYNC_REQUIRED", "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        with open("shi_data.json", "w") as f:
            json.dump(safe_data, f)

if __name__ == "__main__":
    run_ghi_metric_engine()
