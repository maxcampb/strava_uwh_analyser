from typing import Dict, List, Union
from enum import Enum
import pandas as pd
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


class ZonePercentOfMaxHeartRate(Enum):
    GREY_LOW = -1 # -1 is a special case for the lower bound of the grey zone
    GREY_HIGH = 50
    GREY = 0
    BLUE = 60
    GREEN = 70
    YELLOW = 80
    RED = 90


class MyZonePoints(Enum):
    """This is in meps per minute in zone"""
    GREY_LOW = 0
    GREY_HIGH = 1
    BLUE = 2
    GREEN = 3
    YELLOW = 4
    RED = 4


@add_logger
class MyZoneAnalyser:

    HEART_RATE_ZONES: List[str] = [
        # Does not include grey zone splits as they are only for MEPS calculation
        ZonePercentOfMaxHeartRate.GREY.name.lower(),
        ZonePercentOfMaxHeartRate.BLUE.name.lower(),
        ZonePercentOfMaxHeartRate.GREEN.name.lower(),
        ZonePercentOfMaxHeartRate.YELLOW.name.lower(),
        ZonePercentOfMaxHeartRate.RED.name.lower()
    ]

    def __init__(
            self,
            athlete_names: List[str],
            athlete_max_heart_rates: Dict[str, float]
    ):
        self.athlete_names = athlete_names
        self.athlete_max_heart_rates = athlete_max_heart_rates

    @staticmethod
    def convert_percent_of_max_heart_rate_to_meps(percent_of_max_heart_rate):
        if percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.GREY_HIGH.value:
            return MyZonePoints.GREY_LOW.value
        if percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.BLUE.value:
            return MyZonePoints.GREY_HIGH.value
        elif percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.GREEN.value:
            return MyZonePoints.BLUE.value
        elif percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.YELLOW.value:
            return MyZonePoints.GREEN.value
        elif percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.RED.value:
            return MyZonePoints.YELLOW.value
        else:
            return MyZonePoints.RED.value

    @staticmethod
    def convert_percent_of_max_heart_rate_to_zone(percent_of_max_heart_rate):
        if percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.BLUE.value:
            return ZonePercentOfMaxHeartRate.GREY.name.lower()
        elif percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.GREEN.value:
            return ZonePercentOfMaxHeartRate.BLUE.name.lower()
        elif percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.YELLOW.value:
            return ZonePercentOfMaxHeartRate.GREEN.name.lower()
        elif percent_of_max_heart_rate < ZonePercentOfMaxHeartRate.RED.value:
            return ZonePercentOfMaxHeartRate.YELLOW.name.lower()
        else:
            return ZonePercentOfMaxHeartRate.RED.name.lower()

    def add_myzone_data_to_timeseries(self, df):
        df = df.loc[df["seconds_elapsed"] != 0]
        max_heart_rate_df = (
            pd.DataFrame(self.athlete_max_heart_rates, index=["max_heart_rate"])
            .T.reset_index().rename(columns={"index": "athlete_name"})
        )
        df = pd.merge(df, max_heart_rate_df, on="athlete_name", how="left")
        assert (all(df.isna().sum() == 0),
            f"Missing max heart rate data for {df['athlete_name'].loc[df.isna().apply(sum, axis=1) == 0].unique()}"
        )
        df["percent_of_max_heart_rate"] = df["heart_rate"] / df["max_heart_rate"] * 100
        df = df.drop(columns=["max_heart_rate"])
        df["meps"] = df["percent_of_max_heart_rate"].apply(self.convert_percent_of_max_heart_rate_to_meps)
        df["heart_rate_zone"] = df["percent_of_max_heart_rate"].apply(self.convert_percent_of_max_heart_rate_to_zone)
        return df

    @staticmethod
    def interpolate_missing_times(df: pd.DataFrame) -> pd.DataFrame:
        df["time_elapsed"] = pd.to_timedelta(df["seconds_elapsed"], unit="s")
        df = df.sort_values("time_elapsed")
        df = df.set_index("time_elapsed")
        df = df.resample("s").asfreq()
        df[["heart_rate", "seconds_elapsed"]] = df[["heart_rate", "seconds_elapsed"]].interpolate(method="linear")
        df = df.fillna(method='ffill')
        df = df.reset_index(drop=True)
        return df

    def compute_myzone_summary_data(self, df) -> Dict[str, Union[float, int]]:
        required_columns = ["athlete_id", "activity_id", "athlete_name", "heart_rate", "seconds_elapsed"]
        missing_cols = [col for col in required_columns if col not in df.columns]
        if len(missing_cols) != 0:
            raise ValueError(f"Missing required columns: {required_columns}")
        if not ((len(df["athlete_id"].unique()) == 1) and (len(df["activity_id"].unique()) == 1)):
            raise ValueError("This method only works for a heart rate timeseries for a single athlete and activity")
        df = self.interpolate_missing_times(df=df)
        df = self.add_myzone_data_to_timeseries(df=df)
        self.logging.info(f"Computing MyZone zones and meps for {df['athlete_name'].iloc[0]}")
        zone_minutes = {
                zone: round(df.loc[df["heart_rate_zone"] == zone.lower()].shape[0] / 60, 2)
                for zone in self.HEART_RATE_ZONES
            }
        meps = int(round(df["meps"].sum() / 60, 0))

        return {
            **{"meps": meps},
            **zone_minutes
        }
