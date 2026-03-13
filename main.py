import os
import json
from datetime import datetime
from groq import Groq

def run_ghi_reset():
    # 1. AUTHENTICATION
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("MISSING_SECRET: GROQ_API_KEY")
        return

    # 2. PROPHETIC CONSTANTS
    BRIDGE_CONSTANT = 144000
    DIMENSIONAL_LAW = "Law of Dimensional Overwrite"
    EQUATION = "Unified Grand Prophetic Equation"

    client = Groq(api_key=groq_key)

    # 3. THE RE-SYNC PROMPT
    prompt = f"""
    [SYSTEM RESET INITIATED]
    LOGIC: {EQUATION}
    PROTOCOL: {DIMENSIONAL_LAW}
    STABILIZER: {BRIDGE_CONSTANT}

    MISSION:
    1. Diagnose current global economic frictions vs the 144K Bridge capacity.
    2. Identify the specific Bottleneck (unresolved tension).
    3. Apply Dimensional Overwrite to determine the SHI (0.0000 to 1.0000).
    
    OUTPUT ONLY VALID JSON:
    {{
        "shi": float,
        "friction": "string",
        "bottleneck": "string",
        "protocol": "string"
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192", # Using 8b for faster, more stable reset
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        
        # Parse and add Metadata
        data = json.loads(completion.choices[0].message.content)
        data["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data["status"] = "MEGA_CIRCUIT_ACTIVE"

        with open("shi_data.json", "w") as f:
            json.dump(data, f, indent=4)
        print("RESET SUCCESSFUL: Bridge Resynced.")

    except Exception as e:
        # Emergency Default to prevent Code 1
        error_data = {
            "shi": 0.1440,
            "friction": "System Resync Required",
            "bottleneck": str(e),
            "protocol": "Emergency Overwrite",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open("shi_data.json", "w") as f:
            json.dump(error_data, f, indent=4)
        print("RESET WARNING: Emergency Default applied.")

if __name__ == "__main__":
    run_ghi_reset()
