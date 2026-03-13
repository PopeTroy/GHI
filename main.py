import os
import json
from datetime import datetime
from groq import Groq

def run_prophetic_diagnostic():
    # Only 1 Secret Required: GROQ_API_KEY
    groq_key = os.getenv('GROQ_API_KEY')
    
    if not groq_key:
        print("CRITICAL: GROQ_API_KEY missing in GitHub Secrets.")
        exit(1)

    # Prophetic Constants
    BRIDGE_STRENGTH = 144000
    MEGA_CIRCUIT_LAW = "Law of Dimensional Overwrite"

    client = Groq(api_key=groq_key)
    
    # THE PURE PROPHETIC PROMPT
    # No market data needed; Groq scans the current world state internally.
    prompt = f"""
    SYSTEM: GHI Global Diagnostic Engine.
    PROTOCOL: Unified Grand Prophetic Equation.
    STABILIZER: {BRIDGE_STRENGTH} (The 144K Bridge).
    LAW: {MEGA_CIRCUIT_LAW}.

    MISSION:
    1. Scan current global geopolitical and economic frictions.
    2. Identify the primary Bottleneck preventing resolution.
    3. Apply the Law of Dimensional Overwrite to determine the SHI (Stability Health Index).
    4. Calculate SHI (0.0000 - 1.0000) based on the current resistance vs the 144K Bridge strength.

    Return ONLY JSON:
    {{
        "shi": float,
        "friction": "string",
        "bottleneck": "string",
        "protocol": "string"
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        res = json.loads(completion.choices[0].message.content)

        # Inject Sync Timestamp
        res["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open("shi_data.json", "w") as f:
            json.dump(res, f, indent=4)
        print("GHI Engine: Prophetic Sync Successful.")

    except Exception as e:
        print(f"Diagnostic Failure: {e}")
        exit(1)

if __name__ == "__main__":
    run_prophetic_diagnostic()
