import requests
import streamlit as st

# 1. Page Configuration
st.title("🌍 Live Air Quality Monitor")
st.write("Powered by the World Air Quality Index (WAQI) Engine.")

# 2. Input Boxes for User
# Paste your token between the quotes below
WAQI_TOKEN = st.text_input("Enter your WAQI API Token:", type="password")
city_name = st.text_input("Enter a city name (e.g., Tokyo, London, Paris):", "New York")

# 3. Main Logic Button
if st.button("Fetch Real-Time AQI"):
    if not WAQI_TOKEN:
        st.warning("⚠️ Please provide a valid WAQI API token to pull data.")
    else:
        # Build a direct city-search link
        url = f"https://waqi.info{city_name}/?token={WAQI_TOKEN}"
        
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # WAQI sends back a simple 'status' check string
            if data.get("status") == "ok":
                # Isolate the exact core metric directory
                aqi_value = data["data"]["aqi"]
                st.metric(label=f"Current US AQI in {city_name.title()}", value=aqi_value)
                
                # Dynamic Alert Banners
                if aqi_value <= 50:
                    st.success("✅ Clean Air: Air quality is excellent.")
                elif aqi_value <= 100:
                    st.warning("⚠️ Notice: Air quality is moderate.")
                else:
                    st.error("🚨 ALERT: Air quality is unhealthy! Avoid prolonged outdoor activity.")
                    
            else:
                st.error(f"Could not find data for '{city_name}'. Try typing a larger city near you.")
        else:
            st.error(f"API Connection Failed (Error Code: {response.status_code})")
