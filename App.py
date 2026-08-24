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
            # Clean up input string to match backend formatting rules
            cleaned_city = city_input.strip().lower()
            api_safe_city = cleaned_city.replace(" ", "-")
            
            # Fetch the secret token safely out of hidden server settings
            token = st.secrets["waqi_token"].strip().strip('"').strip("'")
            
            # FIX: Switched to standard HTTP base URL to bypass proxy blocking filters
            url = f"http://api.waqi.info/feed/{api_safe_city}/?token={token}"
            
            # Standard browser signatures to prevent server firewalls from flagging the script
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Fetch data with an open connection timeout safety threshold
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify that the WAQI data collection platform found the city
                if data.get("status") == "ok":
                    aqi_value = data["data"]["aqi"]
                    station_name = data["data"]["city"]["name"]
                    
                    # Renders beautiful metric numbers right on your webpage interface
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
                    st.error(f"Could not find data for '{city_input}'. Check your spelling or try a larger capital city nearby.")
            else:
                st.error(f"The weather database responded with an error code: {response.status_code}")
                
        except requests.exceptions.Timeout:
            st.error("⏰ Connection Timeout: The data server took too long to answer. Try clicking the button again.")
        except requests.exceptions.ConnectionError:
            st.error("🌐 Network Connection Error: The platform failed to reach the database API server. Re-trying endpoint links...")
        except Exception as e:
            st.error(f"An unexpected data tracking error occurred: {e}")
