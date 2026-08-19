import os
import json
import re
from datetime import datetime
import openai
from groq import Groq

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
    """Strips markdown wrapping if present."""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()
    return text

def fetch_nvidia_equations(prompt):
    """
    Primary Equation Computation via NVIDIA API Active Models.
    """
    nvidia_key = os.getenv('NVIDIA_API_KEY')
    if not nvidia_key:
        print("[WARNING] NVIDIA_API_KEY missing. Skipping NVIDIA equation solver...")
        return None, None

    nvidia_models = [
        "meta/llama-3.3-70b-instruct",
        "nvidia/llama-3.1-nemotron-70b-instruct",
        "deepseek-ai/deepseek-r1"
    ]
    nv_client = openai.OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=nvidia_key
    )

    for model_name in nvidia_models:
        try:
            print(f"[INFO] Computing Equations via NVIDIA API ({model_name})...")
            completion = nv_client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt + "\nRespond strictly in valid JSON format."}]
            )
            cleaned = clean_json_text(completion.choices[0].message.content)
            return cleaned, f"NVIDIA_{model_name.upper()}"
        except Exception as e:
            print(f"[WARNING] NVIDIA model {model_name} failed: {e}")

    return None, None

def fetch_groq_scan(prompt):
    """
    Global Node Audit via Groq Active Compound Models.
    """
    groq_key = os.getenv('GROQ_API_KEY')
    if not groq_key:
        print("[WARNING] GROQ_API_KEY missing. Skipping Groq compound scan...")
        return None, None

    groq_models = [
        "openai/gpt-oss-120b",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant"
    ]
    client = Groq(api_key=groq_key)

    for g_model in groq_models:
        try:
            print(f"[INFO] Scanning Global Nodes via Groq Compound ({g_model})...")
            completion = client.chat.completions.create(
                model=g_model,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return completion.choices[0].message.content, f"GROQ_{g_model.upper()}"
        except Exception as e:
            print(f"[WARNING] Groq model {g_model} failed: {e}")

    return None, None

def run_ghi_metric_engine():
    prompt = """
    SYSTEM: GHI Logic Engine - Economic Stability & Growth.
    
    DEFINITIONS:
    - Bottlenecks (B): Deviations from stability (Trade barriers, energy chokepoints, high debt).
    - Protocols (P): Growth improvements (Policy reforms, anti-corruption, innovation).
    - Equation: (N * P * F * T) / (B * C)
    
    MISSION: Compute equation metrics and scan for Primary High Impact Location, 3 Bottleneck Nodes (Lowest SHI), and 3 Stable Nodes (Highest SHI).
    
    CRITICAL CONSTRAINT: health_percent MUST BE A FLOAT BETWEEN 0.0 AND 100.0 (DO NOT EXCEED 100).
    
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

    raw_content, active_engine = fetch_nvidia_equations(prompt)
    
    # Fallback to Groq if NVIDIA is unavailable
    if not raw_content:
        raw_content, active_engine = fetch_groq_scan(prompt)

    if not raw_content:
        raise RuntimeError("CRITICAL FAILURE: Both NVIDIA and Groq engines failed to return data.")

    try:
        raw = json.loads(raw_content)
        
        m = raw['metrics']
        shi = (m['N'] * m['P'] * m['F'] * m['T']) / (m['B'] * m['C'] if m['B'] * m['C'] != 0 else 0.00001)

        # STRICT CAP: Enforce 0% to 100% boundary on health_percent
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
