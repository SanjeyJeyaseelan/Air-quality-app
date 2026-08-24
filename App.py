import requests
import streamlit as st

# 1. Page Configuration
st.title("🌍 Live Air Quality Monitor")
st.write("Check real-time air quality index (AQI) values instantly.")

# Create a clean text entry box for your users
city_input = st.text_input("Enter a city name:", "New York")

# 2. Safety Check: Verify that the Streamlit secret token exists
if "waqi_token" not in st.secrets:
    st.error("🔒 Developer Setup Error: The API secret key has not been added to Streamlit settings yet.")
    st.info("To fix this: Go to your Streamlit dashboard -> Click App Settings -> Click Secrets -> Paste: waqi_token = 'your_key_here'")
else:
    if st.button("Fetch Real-Time AQI"):
        try:
            # FIX: Strip spaces entirely so "New York" becomes "newyork"
            cleaned_city = city_input.strip().lower()
            api_safe_city = cleaned_city.replace(" ", "").replace(",", "").replace(".", "")
            
            # Fetch the secret token safely out of hidden server settings
            token = st.secrets["waqi_token"].strip().strip('"').strip("'")
            
            # Build the HTTP request URL
            url = f"http://waqi.info{api_safe_city}/?token={token}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "ok":
                    aqi_value = data["data"]["aqi"]
                    station_name = data["data"]["city"]["name"]
                    
                    # Renders metric numbers on your web app interface
                    st.metric(label=f"Current AQI in {city_input.title()}", value=aqi_value)
                    st.caption(f"📍 Reporting Station: {station_name}")
                    
                    # Threshold Alerts
                    if aqi_value <= 50:
                        st.success("✅ Clean Air: Air quality is excellent today.")
                    elif aqi_value <= 100:
                        st.warning("⚠️ Notice: Air quality is moderate.")
                    else:
                        st.error("🚨 ALERT: Air quality is unhealthy! Avoid prolonged outdoor activity.")
                else:
                    st.error(f"Could not find data for '{city_input}'. Try typing a major city name directly (e.g., 'shanghai', 'london', 'paris').")
            else:
                st.error(f"The weather database responded with an error code: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.error("⏰ Connection Timeout: The data server took too long to answer. Try clicking the button again.")
        except requests.exceptions.ConnectionError:
            st.error("🌐 Network Connection Error: The platform failed to reach the database API server.")
        except Exception as e:
            st.error(f"An unexpected data tracking error occurred: {e}")
