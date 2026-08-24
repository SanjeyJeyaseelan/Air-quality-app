import urllib.parse
import requests
import streamlit as st

# 1. Page Configuration
st.title("🌍 Live Air Quality Monitor")
st.write("Check real-time air quality index (AQI) values instantly.")

# Clean user input box
city_input = st.text_input("Enter a city name:", "New York")

# 2. Safety Check: Verify that the Streamlit secret token exists
if "waqi_token" not in st.secrets:
    st.error("🔒 Developer Setup Error: The API secret key has not been added to Streamlit settings yet.")
    st.info("To fix this: Go to your Streamlit dashboard -> Click App Settings -> Click Secrets -> Paste: waqi_token = 'your_key_here'")
else:
    if st.button("Fetch Real-Time AQI"):
        try:
            # Clean and strip any accidental whitespace from user inputs
            cleaned_city = city_input.strip()
            safe_city = urllib.parse.quote(cleaned_city)
            
            # Fetch the raw token string safely out of hidden server settings
            raw_token = st.secrets["waqi_token"]
            cleaned_token = str(raw_token).strip().strip('"').strip("'")
            
            # Build the request URL explicitly with safe components
            base_url = "https://api.waqi.info"
            endpoint = f"/feed/{safe_city}/"
            query_string = f"?token={cleaned_token}"
            full_url = base_url + endpoint + query_string
            
            # Use an explicit timeout window to prevent proxy drop disconnects
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "ok":
                    aqi_value = data["data"]["aqi"]
                    
                    # Renders metric visualization right on your web application
                    st.metric(label=f"Current AQI in {cleaned_city.title()}", value=aqi_value)
                    
                    # Threshold Alerts
                    if aqi_value <= 50:
                        st.success("✅ Clean Air: Air quality is excellent today.")
                    elif aqi_value <= 100:
                        st.warning("⚠️ Notice: Air quality is moderate.")
                    else:
                        st.error("🚨 ALERT: Air quality is unhealthy! Avoid prolonged outdoor activity.")
                else:
                    st.error(f"Could not find data for '{cleaned_city}'. Check your spelling or try a larger city.")
            else:
                st.error(f"The weather database responded with an error page. (Status Code: {response.status_code})")
                
        except requests.exceptions.Timeout:
            st.error("⏰ Connection Timeout: The remote data server took too long to answer. Try clicking the button again.")
        except requests.exceptions.ConnectionError:
            st.error("🌐 Network Connection Error: The Streamlit cloud platform failed to reach the database API server. Please retry.")
        except Exception as e:
            st.error(f"An unexpected data layout error occurred: {e}")
