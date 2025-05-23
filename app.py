# Freight Whisperer: Streamlit App for Broker Quote Parsing (OpenAI SDK v1.x Compatible)

import streamlit as st
import openai
import json

# Set the page config
st.set_page_config(page_title="Freight Whisperer")

# App Title
st.title("🚢 Freight Whisperer")
st.subheader("Paste a broker message, get structured trade info + price signal")

# Input for OpenAI API Key
openai_api_key = st.secrets.get("openai_api_key") or st.text_input("Enter your OpenAI API Key", type="password")

# Text input area for broker quote
quote = st.text_area(
    "Paste Broker Quote", 
    height=200, 
    value="MV Blue Whale, Supramax 56k DWT, open CJK 25-27 May, 1st leg trip via NoPac to Singapore–Japan range, redelivery Japan, $16,250/d basis dop. Charterers: Bunge."
)

# Button to decode quote
if st.button("Decode Quote") and openai_api_key:
    prompt = f"""Extract the following fields from this broker message:
- Vessel name
- Vessel type
- DWT
- Open port
- Laycan
- Route
- Cargo (if any)
- Redelivery port
- Daily rate (USD)
- Charterer (if any)
- Sentiment (bullish, neutral, bearish)

Message: {quote}

Return as JSON."""

    try:
        client = openai.OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        st.subheader("Extracted Output")
        st.json(json.loads(result))
    except Exception as e:
        st.error(f"Error: {e}")

