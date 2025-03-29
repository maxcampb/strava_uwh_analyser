import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from strava_uwh_analyser.extractors.activities_extractor import ActivitiesExtractor
from strava_uwh_analyser.extractors.athletes_extractor import AthletesExtractor
from strava_uwh_analyser.analysers.myzone_analyser import MyZoneAnalyser
from strava_uwh_analyser.utils.base_classes import BaseReport
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


@add_logger
class ExampleReport(BaseReport):
    """ This is an example report that demonstrates how to create a report you should create your own report"""
    report_name = "example_uwh_report"
    ATHLETE_NAMES = [
        "max_campbell",
    ]
    EMAIL_RECIPIENTS = {
        "max_campbell": "maxcampb@hotmail.com",
    }

    def __init__(
            self,
            save_locally: bool = False,
            send_report_email: bool = False,
    ):
        super().__init__(save_locally=save_locally, send_report_email=send_report_email)
        self.start_date = pd.to_datetime(self.base_variables.run_date - relativedelta(days=14))
        self.end_date = pd.to_datetime(self.base_variables.run_date)
        self.athlete_names = self.ATHLETE_NAMES

        # Get data using extractors
        self.athletes = AthletesExtractor(
            athlete_names=self.athlete_names,
            load_athlete_configs=True,
        ).run()

        self.data = ActivitiesExtractor(
            start_date=self.start_date,
            end_date=self.end_date,
            athlete_names=self.athlete_names
        ).run()

    def get_start_date(self) -> datetime.datetime:
        """Get the start date for the report"""
        return pd.to_datetime(self.base_variables.run_date - relativedelta(days=7))

    def get_end_date(self) -> datetime.datetime:
        """Get the end date for the report"""
        return pd.to_datetime(self.base_variables.run_date)

    def process_activity(self, activity) -> pd.DataFrame:
        activity_df = pd.DataFrame({
            "athlete_name": activity.athlete_name,
            "athlete_id": activity.athlete_id,
            "start_time": activity.start_time,
            "activity_name": activity.activity_name,
            "moving_time": activity.moving_time,
            "elasped_time": activity.elasped_time,
            "distance": activity.distance,
            "sport_type": activity.sport_type
        }, index=[0])

        if activity.heart_rate_data is not None:
            heart_rate_data = activity.heart_rate_data
            activity_df["average_heart_rate"] = heart_rate_data["heart_rate"].mean()
            activity_df["max_heart_rate"] = heart_rate_data["heart_rate"].max()

        assert activity_df.shape[0] == 1

        return activity_df

    def generate_report(self) -> pd.DataFrame:
        self.logger.info(f"Generating report between {self.start_date} and {self.end_date} ")
        activity_data = []
        for activity in self.data:
            activity_data.append(self.process_activity(activity))

        activity_df = pd.concat(activity_data).reset_index(drop=True)

        return activity_df .reset_index()
