import requests
import streamlit as st

# 1. App Title and UI Elements
st.title("🌍 Live Air Quality Monitor")
st.write("Fetching real-time environmental metrics instantly via the open-access OpenAQ network.")

# Clean user input box
city_input = st.text_input("Enter a major city name:", "New York")

if st.button("Fetch Real-Time AQI"):
    try:
        # Clean input text string formatting
        cleaned_city = city_input.strip().title()
        
        # OpenAQ uses direct parameters and doesn't require API key validation
        url = "https://openaq.org"
        params = {
            "city": cleaned_city,
            "limit": 1,
            "parameter": "pm25"
        }
        
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        # Execute the network query
        response = requests.get(url, params=params, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify if the global database contains tracking records for this city
            if data.get("results") and len(data["results"]) > 0:
                # Target the core metrics dictionary folder
                station_data = data["results"][0]
                location_name = station_data.get("location", "Local Station")
                
                # Extract the individual particulate reading element
                measurements = station_data.get("measurements", [])
                if measurements:
                    pm25_value = measurements[0].get("value", 0)
                    unit = measurements[0].get("unit", "µg/m³")
                    
                    # Display metrics visually
                    st.metric(label=f"Current PM2.5 Concentration in {cleaned_city}", value=f"{pm25_value} {unit}")
                    st.caption(f"📍 Reporting Station: {location_name}")
                    
                    # Convert raw particulate concentration into dynamic warning panels
                    if pm25_value <= 12.0:
                        st.success("✅ Clean Air: Air quality is healthy.")
                    elif pm25_value <= 35.4:
                        st.warning("⚠️ Notice: Air quality is moderate.")
                    else:
                        st.error("🚨 ALERT: Air quality is unhealthy! Avoid prolonged outdoor activity.")
                else:
                    st.warning("The local station is active but hasn't updated its particulate readings recently.")
            else:
                st.error(f"Could not locate active open-source monitoring data for '{city_input}'. Try typing another major global city (e.g., 'London', 'Delhi', 'Los Angeles').")
        else:
            st.error(f"External service connection error (Status Code: {response.status_code})")
            
    except requests.exceptions.Timeout:
        st.error("⏰ Connection Timeout: The server took too long to answer. Try clicking the button again.")
    except requests.exceptions.ConnectionError:
        st.error("🌐 Network Connection Error: Streamlit Cloud failed to route traffic to this endpoint.")
    except Exception as e:
        st.error(f"An unexpected tracking data error occurred: {e}")
