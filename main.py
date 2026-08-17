import os
import json
from datetime import datetime
from groq import Groq
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

def fetch_model_completion(prompt):
    """
    Executes inference using Groq specdec first.
    Fails over seamlessly across NVIDIA API models if Groq fails or is unavailable.
    """
    groq_key = os.getenv('GROQ_API_KEY')
    nvidia_key = os.getenv('NVIDIA_API_KEY')

    # Primary Route: Groq SpecDec
    if groq_key:
        try:
            print("[INFO] Initiating primary audit scan via Groq (llama-3.3-70b-specdec)...")
            client = Groq(api_key=groq_key)
            completion = client.chat.completions.create(
                model="llama-3.3-70b-specdec",
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return completion.choices[0].message.content, "GROQ_SPECDEC"
        except Exception as e:
            print(f"[WARNING] Primary Groq engine failed: {e}. Executing failover sequence...")

    # Secondary Route: NVIDIA API Multi-Model Cascade
    if nvidia_key:
        nvidia_models = [
            "meta/llama-3.3-70b-instruct",
            "deepseek-ai/deepseek-r1",
            "nvidia/llama-3.1-nemotron-70b-instruct"
        ]
        nv_client = openai.OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=nvidia_key
        )
        for model_name in nvidia_models:
            try:
                print(f"[INFO] Invoking Failover: Engaging NVIDIA API ({model_name})...")
                completion = nv_client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt + "\nRespond strictly in raw JSON."}],
                    response_format={"type": "json_object"} if "deepseek" not in model_name else None
                )
                raw_text = completion.choices[0].message.content
                # Strip markdown code blocks if present
                if "```json" in raw_text:
                    raw_text = raw_text.split("```json")[1].split("```")[0].strip()
                elif "```" in raw_text:
                    raw_text = raw_text.split("```")[1].split("```")[0].strip()
                return raw_text, f"NVIDIA_{model_name.upper()}"
            except Exception as e:
                print(f"[WARNING] NVIDIA model {model_name} failed: {e}. Trying next failover model...")

    raise RuntimeError("CRITICAL FAILURE: All Groq and NVIDIA API inference engines failed.")

def run_ghi_metric_engine():
    prompt = """
    SYSTEM: GHI Logic Engine - Economic Stability & Growth.
    
    DEFINITIONS:
    - Bottlenecks (B): Deviations from stability (Trade barriers, energy chokepoints, high debt).
    - Protocols (P): Growth improvements (Policy reforms, anti-corruption, innovation).
    - Equation: (N * P * F * T) / (B * C)
    
    MISSION: Identify High Impact Location, 3 Bottleneck Nodes, and 3 Stable (High SHI) Nodes.
    
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
        raw_content, active_engine = fetch_model_completion(prompt)
        raw = json.loads(raw_content)
        
        m = raw['metrics']
        shi = (m['N'] * m['P'] * m['F'] * m['T']) / (m['B'] * m['C'] if m['B'] * m['C'] != 0 else 0.00001)

        health_val = float(raw['health_percent'])
        tactical_data = compute_divine_tactics(health_val)

        output_data = {
            "shi": round(shi, 5),
            "health_percent": health_val,
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
        
        print(f"Sync Success via [{active_engine}]: {output_data['location']} - Collapse Type: {output_data['collapse_type']}")

    except Exception as e:
        print(f"Engine Failure: {e}")
        exit(1)

if __name__ == "__main__":
    run_ghi_metric_engine()
