import os
import json
from datetime import datetime
import openai

def compute_divine_tactics(health_val):
    """
    Evaluates system operational state using high-order ocular reserves
    and Tailed Beast chakra stability matrix.
    """
    if health_val >= 65:
        ocular_ability = "JOUGAN_DIMENSIONAL_PREDICTION"
        chakra_level = "EIGHT_TAILS_SEALED"
    elif health_val >= 50:
        ocular_ability = "SHARINGAN_THREE_TOMOE"
        chakra_level = "FOUR_TAILS_RESONANCE"
    elif health_val > 20:
        ocular_ability = "MANGEKYO_SPACE_TIME_ISOLATION"
        chakra_level = "NINE_TAILS_KAMA_OVERDRIVE"
    else:
        ocular_ability = "RINNEGAN_ALMIGHTY_PUSH_REBOOT"
        chakra_level = "TEN_TAILS_COLLAPSE_IMPERATIVE"

    return {
        "active_eye": ocular_ability,
        "tailed_beast_chakra": chakra_level,
        "kama_compression_ratio": round(1.0 - (health_val / 100.0), 4),
        "genjutsu_defense_status": "ACTIVE_UNPERVERTED"
    }

def clean_json_text(text):
    """Strips markdown block wrappers if present."""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text

def fetch_nvidia_nim_cascade(prompt):
    """
    Executes GHI metrics calculation and node scanning using NVIDIA NIM microservice 
    endpoints with automated failover across top-tier models.
    """
    nvidia_key = os.getenv('NVIDIA_API_KEY')
    if not nvidia_key:
        print("CRITICAL ERROR: NVIDIA_API_KEY missing.")
        exit(1)

    # High-performance NVIDIA NIM models from your verified dashboard catalog
    nvidia_nim_models = [
        "mistralai/mistral-large-4",
        "nvidia/nemotron-3.5-super-vl-120b-a12b",
        "nvidia/nemotron-3.5-lightning-30b-a3b",
        "nvidia/nemotron-3.5-bolt-e4b"
    ]

    nv_client = openai.OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=nvidia_key,
        timeout=20.0
    ]

    for model_name in nvidia_nim_models:
        try:
            print(f"[INFO] Invoking NVIDIA NIM Microservice ({model_name})...")
            completion = nv_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt + "\nRespond strictly in valid raw JSON format without markdown preamble."}],
                temperature=0.2
            )
            cleaned = clean_json_text(completion.choices[0].message.content)
            return cleaned, f"NVIDIA_NIM_{model_name.upper().replace('/', '_')}"
        except Exception as e:
            print(f"[WARNING] NVIDIA NIM Model {model_name} failed: {e}. Cascading...")

    raise RuntimeError("CRITICAL FAILURE: All NVIDIA NIM Microservice inference engines failed.")

def run_ghi_metric_engine():
    prompt = """
    SYSTEM: GHI Logic Engine - Economic Stability & Growth.
    
    DEFINITIONS:
    - Bottlenecks (B): Deviations from stability (Trade barriers, energy chokepoints, high debt).
    - Protocols (P): Growth improvements (Policy reforms, anti-corruption, innovation).
    - Equation: (N * P * F * T) / (B * C)
    
    MISSION: Identify High Impact Location, 3 Bottleneck Nodes, and 3 Stable (High SHI) Nodes.
    
    CRITICAL CONSTRAINT: health_percent MUST BE A FLOAT STRICTLY BETWEEN 0.0 AND 100.0 (DO NOT EXCEED 100).
    
    REQUIRED OUTPUT JSON:
    {
        "metrics": {"N": 1.44, "P": float, "F": float, "T": float, "B": float, "C": float},
        "health_percent": float,
        "primary_high_impact": "CITY, COUNTRY",
        "collapse_type": "HYPER-INFLATION / GRID COLLAPSE / CIVIL UNREST / SUPPLY CHAIN BREAK",
        "collapse_timer": "string (e.g. 72:14:05)",
        "bottleneck_nodes": [{"loc": "CITY, COUNTRY", "deviation": "string"}],
        "high_shi_nodes": [{"loc": "CITY, COUNTRY", "protocol": "string"}],
        "scroller_feed": "string"
    }
    """

    try:
        raw_content, active_engine = fetch_nvidia_nim_cascade(prompt)
        raw = json.loads(raw_content)
        
        m = raw['metrics']
        shi = (m['N'] * m['P'] * m['F'] * m['T']) / (m['B'] * m['C'] if m['B'] * m['C'] != 0 else 0.00001)

        # Enforce strict 0% to 100% boundary to prevent over-100% visual errors
        raw_health = float(raw['health_percent'])
        health_val = min(100.0, max(0.0, raw_health))

        tactical_data = compute_divine_tactics(health_val)

        output_data = {
            "shi": round(shi, 5),
            "health_percent": round(health_val, 2),
            "location": raw['primary_high_impact'].upper(),
            "collapse_type": raw['collapse_type'].upper(),
            "collapse_timer": raw['collapse_timer'],
            "bottlenecks": raw['bottleneck_nodes'],
            "high_shi": raw['high_shi_nodes'],
            "scroller_feed": f"CRITICAL: {raw['primary_high_impact'].upper()} TARGETED FOR {raw['collapse_type'].upper()} | {raw['scroller_feed'].upper()}",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "formula_metrics": m,
            "engine_active": active_engine,
            "shinobi_tactics": tactical_data
        }

        with open("shi_data.json", "w") as f:
            json.dump(output_data, f, indent=4)
        
        print(f"Sync Success via [{active_engine}]: {output_data['location']} - Health: {output_data['health_percent']}%")

    except Exception as e:
        print(f"Engine Failure: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
