from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


class CongestionAnalyzer:
    @staticmethod
    def calculate_hourly_congestion(
        flight_infos: list, reference_date: datetime
    ) -> dict[str, int]:
        histogram = {}
        for hour in range(24):
            start = reference_date.replace(hour=hour, minute=0, second=0, microsecond=0)
            end = start + timedelta(hours=1)
            passengers = sum(
                flight["estimated_passengers"]
                for flight in flight_infos
                if start <= datetime.fromisoformat(flight["arrival_time"]) < end
            )
            histogram[start.strftime("%H:%M")] = passengers
        return histogram

    @staticmethod
    def create_congestion_plot(congestion: dict, return_fig=False):
        fig, ax = plt.subplots(figsize=(12, 6))
        hours = list(congestion.keys())
        counts = list(congestion.values())

        ax.bar(hours, counts)
        ax.set_title("Hourly Congestion for Non-Privileged Flights")
        ax.set_xlabel("Hour of Day")
        ax.set_ylabel("Estimated Passengers")
        plt.xticks(rotation=45)
        plt.tight_layout()

        if return_fig:
            return fig
        plt.show()
