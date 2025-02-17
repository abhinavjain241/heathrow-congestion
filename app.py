import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from flight_data import FlightDataFetcher
from congestion_analyzer import CongestionAnalyzer

def main():
    st.title("Heathrow Airport Congestion Analyzer")
    
    # Date selection
    min_date = datetime.now()
    max_date = min_date + timedelta(days=14)
    selected_date = st.date_input(
        "Select Date",
        min_value=min_date,
        max_value=max_date,
        value=min_date + timedelta(days=5)
    )
    
    # Initialize our classes
    fetcher = FlightDataFetcher()
    analyzer = CongestionAnalyzer()
    
    if st.button("Analyze Congestion"):
        with st.spinner("Fetching flight data..."):
            # Fetch and process data
            arrivals_data = fetcher.get_arrivals(selected_date)
            all_flights = fetcher.parse_response(arrivals_data)
            non_privileged_flights = fetcher.filter_non_privileged_flights(all_flights)
            
            # Calculate congestion
            congestion = analyzer.calculate_hourly_congestion(
                non_privileged_flights, 
                datetime.combine(selected_date, datetime.min.time())
            )
            
            # Create DataFrames
            df_all = pd.DataFrame(all_flights)
            df_non_privileged = pd.DataFrame(non_privileged_flights)
            
            # Display results
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Congestion Chart")
                fig = analyzer.create_congestion_plot(congestion, return_fig=True)
                st.pyplot(fig)
            
            with col2:
                st.subheader("Congestion Data")
                st.dataframe(pd.DataFrame(list(congestion.items()), 
                           columns=['Hour', 'Estimated Passengers']))
            
            st.subheader("Flight Details")
            tabs = st.tabs(["All Flights", "Non-Privileged Flights"])
            
            with tabs[0]:
                st.dataframe(df_all)
            
            with tabs[1]:
                st.dataframe(df_non_privileged)

if __name__ == "__main__":
    main() 