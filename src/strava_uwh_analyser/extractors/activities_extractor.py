from typing import Optional, List, Dict
import datetime
import pandas as pd
from strava_uwh_analyser.utils.base_classes import StravaExtractor
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


class ProcessedActivityData:

    def __init__(
            self,
            raw_strava_activity,
            heart_rate_df: pd.DataFrame,
            athlete_name: str,
    ):
        self.athlete_id = raw_strava_activity.athlete.id
        self.athlete_name = athlete_name
        self.start_time = raw_strava_activity.start_date
        self.activity_id = raw_strava_activity.id
        self.activity_name = raw_strava_activity.name
        self.moving_time = raw_strava_activity.moving_time / 60
        self.elasped_time = raw_strava_activity.elapsed_time / 60
        self.distance = raw_strava_activity.distance / 1000
        self.sport_type = raw_strava_activity.sport_type.root
        self.heart_rate_data = heart_rate_df


@add_logger
class ActivitiesExtractor(StravaExtractor):

    def __init__(
            self,
            start_date: datetime.datetime,
            end_date: datetime.datetime,
            athlete_names: Optional[List[str]] = None,
    ):
        self.client = None
        self.start_date = start_date
        self.end_date = end_date
        if athlete_names is None:
            self.athlete_names = [
                athlete_name
                for athlete_name, creds in self.strava_handler.credentials.items()
                if creds is not None
            ]
        else:
            self.athlete_names = athlete_names

    def extract(self) -> Dict[str, List[ProcessedActivityData]]:
        self.logger.info("Extracting activities data ...")
        activities_data = {}
        for athlete_name in self.athlete_names:
            self.client = self.strava_handler.get_configured_athlete_client(athlete_name)
            activities = self.client.get_activities(
                after=self.start_date,
                before=self.end_date,
            )
            activities_data[athlete_name] = self.extract_from_activities_iterator(activities, athlete_name)
        self.logger.info("Extracting activities data was successful")

        return activities_data

    def extract_from_activities_iterator(self, activities, athlete_name) -> List[ProcessedActivityData]:
        activity_data = []
        for activity in activities:
            heart_rate_df = self.extract_heart_rate_data(activity_id=activity.id)
            activity_data.append(
                ProcessedActivityData(
                    raw_strava_activity=activity,
                    heart_rate_df=heart_rate_df,
                    athlete_name=athlete_name,
                )
            )

        return activity_data

    def extract_heart_rate_data(self, activity_id: int) -> pd.DataFrame:
        # Time stream is in seconds  https://developers.strava.com/docs/reference/#api-models-TimeStream
        try:
            activity_streams = self.client.get_activity_streams(
                activity_id, types=["heartrate", "time"], resolution="high"
            )
            heart_rate_df = pd.DataFrame({
                "heart_rate": activity_streams["heartrate"].data,
                "seconds_elapsed": activity_streams["time"].data
            })
        except Exception:
            heart_rate_df = None

        return heart_rate_df

    def transform(self, data: Dict[str, List[ProcessedActivityData]]) -> List[ProcessedActivityData]:
        self.logger.info("Transforming activities data")

        return [
            activity
            for athlete_activities in data.values()
            for activity in athlete_activities
        ]
