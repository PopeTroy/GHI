import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_metric_engine():
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key: return

    client = Groq(api_key=groq_key)

    # UPDATED MISSION: Identify specific Global Bottlenecks vs Protocols
    prompt = """
    SYSTEM: GHI Global Diagnostic Intelligence.
    MISSION: Identify the 3 biggest global Bottlenecks (Red Tensions) and 3 corresponding Protocols (Green Solutions).
    
    EQUATION: (N * P * F * T) / (B * C)
    
    OUTPUT REQUIREMENTS:
    - Summarize the Bottlenecks as high-impact news-style alerts.
    - Summarize the Protocols as GHI-driven resolution strategies.
    
    Return ONLY JSON:
    {
        "metrics": {"N": float, "P": float, "F": float, "T": float, "B": float, "C": float},
        "friction_report": "TEXT FOR SCROLLER",
        "protocol_report": "TEXT FOR SCROLLER",
        "bottleneck": "string",
        "protocol": "string"
    }
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        raw = json.loads(completion.choices[0].message.content)
        m = raw.get('metrics', {})

        # RAW CALCULATION
        N, P, F, T = float(m.get('N', 1)), float(m.get('P', 1)), float(m.get('F', 1)), float(m.get('T', 1))
        B, C = float(m.get('B', 1)), float(m.get('C', 1))
        denominator = (B * C) if (B * C) != 0 else 0.00001
        calculated_shi = (N * P * F * T) / denominator

        output = {
            "shi": round(calculated_shi, 5),
            "scroller_feed": f"🔴 BOTTLENECKS: {raw['friction_report']} 🟢 PROTOCOLS: {raw['protocol_report']}",
            "status": "MEGA_CIRCUIT_ACTIVE",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": {"N": N, "P": P, "F": F, "T": T, "B": B, "C": C}
        }

        with open("shi_data.json", "w") as f:
            json.dump(output, f, indent=4)
        print(f"GHI Intelligence Sync: Success.")

    except Exception as e:
        print(f"Logic Error: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
