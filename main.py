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

def fetch_nvidia_cascade(prompt):
    """
    Executes GHI metrics calculation strictly using verified production 
    NVIDIA endpoints with a hard 10-second request timeout.
    """
    nvidia_key = os.getenv('NVIDIA_API_KEY')
    if not nvidia_key:
        raise ValueError("CRITICAL ERROR: NVIDIA_API_KEY missing from environment secrets.")

    # High-speed production endpoints on NVIDIA API
    nvidia_models = [
        "meta/llama-3.3-70b-instruct",
        "nvidia/llama-3.1-nemotron-70b-instruct",
        "mistralai/mistral-large-2-instruct"
    ]

    nv_client = openai.OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=nvidia_key,
        timeout=10.0  # Prevents long hanging requests
    )

    for model_name in nvidia_models:
        try:
            print(f"[INFO] Executing scan via NVIDIA ({model_name})...")
            completion = nv_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt + "\nRespond strictly in valid raw JSON format."}],
                temperature=0.2
            )
            cleaned = clean_json_text(completion.choices[0].message.content)
            return cleaned, f"NVIDIA_{model_name.upper()}"
        except Exception as e:
            print(f"[WARNING] NVIDIA Model {model_name} skipped/failed: {e}")

    raise RuntimeError("CRITICAL FAILURE: All NVIDIA inference engines failed.")

def run_ghi_metric_engine():
    prompt = """
    SYSTEM: GHI Logic Engine - Global Economic Stability & Architectural Audit.
    
    DEFINITIONS:
    - Bottlenecks (B): Deviations from stability (Trade barriers, energy chokepoints, high debt).
    - Protocols (P): Growth improvements (Policy reforms, anti-corruption, innovation).
    - Equation: (N * P * F * T) / (B * C)
    
    MISSION: Compute equation metrics and identify Primary High Impact Location, 3 Bottleneck Nodes (Lowest SHI), and 3 Stable Nodes (Highest SHI).
    
    CRITICAL CONSTRAINTS: 
    - health_percent MUST BE A FLOAT STRICTLY BETWEEN 0.0 AND 100.0 (DO NOT EXCEED 100).
    
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
        raw_content, active_engine = fetch_nvidia_cascade(prompt)
        raw = json.loads(raw_content)
        
        m = raw['metrics']
        shi = (m['N'] * m['P'] * m['F'] * m['T']) / (m['B'] * m['C'] if m['B'] * m['C'] != 0 else 0.00001)

        # Enforce strict 0% to 100% boundary
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
        
        print(f"Sync Success via [{active_engine}]: Location: {output_data['location']} - Health: {output_data['health_percent']}%")

    except Exception as e:
        print(f"Engine Failure: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
