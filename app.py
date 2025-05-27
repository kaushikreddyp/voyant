# Freight Whisperer: Streamlit App Using Groq (No Referer Restrictions)

import streamlit as st
import requests
import json

# Set the page config
st.set_page_config(page_title="Freight Whisperer")

# App Title
st.title("🚢 Freight Whisperer")
st.subheader("Paste a broker message, get structured trade info + price signal")

# Groq API key input
api_key = st.secrets.get("groq_api_key") or st.text_input("Enter your Groq API Key", type="password")

# Text input area for broker quote
quote = st.text_area(
    "Paste Broker Quote", 
    height=200, 
    value="MV Blue Whale, Supramax 56k DWT, open CJK 25-27 May, 1st leg trip via NoPac to Singapore–Japan range, redelivery Japan, $16,250/d basis dop. Charterers: Bunge."
)

# Button to decode quote
if st.button("Decode Quote") and api_key:
    prompt = f"""Extract the following fields from this broker message:
- Vessel name
- Vessel type
- DWT (if missing, infer approximate from vessel type)
- Open port
- Laycan (date range if possible, else say 'Not specified')
- Route (origin to destination)
- Cargo (if any)
- Redelivery port
- Daily rate (USD)
- Charterer (if any)
- Market sentiment (bullish, neutral, bearish)
- Confidence level for each field (High, Medium, Low)

Avoid using generic placeholders like 'Prompt Supra' as vessel name.
If fields are missing, try to infer or explain why not extracted.

Message: {quote}

Return result as JSON with keys: vessel_name, vessel_type, dwt, open_port, laycan, route, cargo, redelivery_port, rate_usd_day, charterer, sentiment, and confidence_scores (dict)."""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            st.subheader("Extracted Output")
            st.json(json.loads(result))
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Request failed: {e}")


