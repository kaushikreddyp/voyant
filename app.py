# Freight Whisperer: Streamlit App Using OpenRouter with Hardcoded API Key (for testing)

import streamlit as st
import openai
import json

# Set the page config
st.set_page_config(page_title="Freight Whisperer")

# App Title
st.title("🚢 Freight Whisperer")
st.subheader("Paste a broker message, get structured trade info + price signal")

# Initialize OpenRouter with hardcoded API key for testing
client = openai.OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# Text input area for broker quote
quote = st.text_area(
    "Paste Broker Quote", 
    height=200, 
    value="MV Blue Whale, Supramax 56k DWT, open CJK 25-27 May, 1st leg trip via NoPac to Singapore–Japan range, redelivery Japan, $16,250/d basis dop. Charterers: Bunge."
)

# Button to decode quote
if st.button("Decode Quote"):
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

    try:
        response = client.chat.completions.create(
            model="mistralai/mixtral-8x7b",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        st.subheader("Extracted Output")
        st.json(json.loads(result))
    except Exception as e:
        st.error(f"Error: {e}")


