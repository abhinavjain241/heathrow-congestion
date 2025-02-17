from datetime import datetime, timedelta
import pandas as pd

from flight_data import FlightDataFetcher
from congestion_analyzer import CongestionAnalyzer

if __name__ == "__main__":
    fetcher = FlightDataFetcher()
    analyzer = CongestionAnalyzer()
    reference_date = datetime.now() + timedelta(days=5)

    # Fetch and process data
    arrivals_data = fetcher.get_arrivals(reference_date)
    all_flights = fetcher.parse_response(arrivals_data)
    non_privileged_flights = fetcher.filter_non_privileged_flights(all_flights)
    congestion = analyzer.calculate_hourly_congestion(
        non_privileged_flights, reference_date
    )

    # Display results
    print("All flights:")
    print(pd.DataFrame(all_flights))
    print("\nNon-privileged flights:")
    print(pd.DataFrame(non_privileged_flights))
    print("\nHourly congestion for non-privileged flights:")
    print(congestion)

    analyzer.create_congestion_plot(congestion)
