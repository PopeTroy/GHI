import os
import json
import requests
from datetime import datetime
from groq import Groq

def get_market_tension(api_key):
    # Checking Gold (XAU) as a primary friction indicator
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=GLD&apikey={api_key}"
    try:
        r = requests.get(url).json()
        price_change = float(r["Global Quote"]["09. change"])
        return abs(price_change) # Higher volatility = Higher tension
    except:
        return 0.5 # Default tension constant

def run_ghi_diagnostic():
    # Load Secrets from GitHub
    groq_key = os.getenv('GROQ_API_KEY')
    dedicated_key = os.getenv('DEDICATED_KEY') # Add your stock key to GitHub Secrets!
    
    client = Groq(api_key=groq_key)
    tension_index = get_market_tension(dedicated_key)

    # The Diagnostic Prompt for Groq
    prompt = f"""
    Analyze the current global state: Tension Index is {tension_index}.
    Identify a specific World Friction (Trade, Conflict, or Energy).
    Identify a Bottleneck (Missing Protocol or Obstruction).
    Calculate the SHI (Stability Health Index) between 0.0000 and 1.0000.
    Return ONLY a JSON object: 
    {{"shi": float, "friction": "string", "bottleneck": "string", "protocol": "string"}}
    """

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    res = json.loads(completion.choices[0].message.content)

    # Compile the 144K Bridge Data
    final_data = {
        "shi": res['shi'],
        "active_problem": res['friction'],
        "bottleneck": res['bottleneck'],
        "protocol": res['protocol'],
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    with open("shi_data.json", "w") as f:
        json.dump(final_data, f, indent=4)

if __name__ == "__main__":
    run_ghi_diagnostic()
