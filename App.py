import requests
import streamlit as st

# 1. Page Configuration
st.title("🌍 Live Air Quality Monitor")
st.write("Check real-time air quality index (AQI) values instantly.")

# Clean user input box
city_name = st.text_input("Enter a city name:", "New York")

if st.button("Fetch Real-Time AQI"):
    try:
        # Pulls the secret token automatically from the backend
        WAQI_TOKEN = st.secrets["waqi_token"]
        
        # Connect directly to the WAQI feed URL
        url = f"https://waqi.info{city_name}/?token={WAQI_TOKEN}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get("status") == "ok":
                aqi_value = data["data"]["aqi"]
                
                # Visual Dashboard Metrics
                st.metric(label=f"Current AQI in {city_name.title()}", value=aqi_value)
                
                # Threshold Alerts
                if aqi_value <= 50:
                    st.success("✅ Clean Air: Air quality is excellent today.")
                elif aqi_value <= 100:
                    st.warning("⚠️ Notice: Air quality is moderate.")
                else:
                    st.error("🚨 ALERT: Air quality is unhealthy! Avoid prolonged outdoor activity.")
            else:
                st.error(f"Could not find data for '{city_name}'. Check your spelling or try a larger city.")
        else:
            st.error("Could not connect to the weather service data feed.")
            
    except KeyError:
        st.error("Developer Setup Error: The API secret key has not been added to Streamlit settings yet.")
