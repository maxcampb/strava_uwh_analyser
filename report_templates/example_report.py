import datetime
from typing import List
import pandas as pd
from dateutil.relativedelta import relativedelta

from strava_uwh_analyser.extractors.activities_extractor import ActivitiesExtractor
from strava_uwh_analyser.extractors.athletes_extractor import AthletesExtractor
from strava_uwh_analyser.utils.base_classes import BaseReport
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


@add_logger
class ReportTemplate(BaseReport):

    ATHLETE_NAMES: List[str] = [
        "athlete_1",
        "athelete_2"
    ]

    def __init__(
            self,
            save_locally: bool = False,
            send_report_email: bool = False,
    ):
        super().__init__(save_locally=save_locally, send_report_email=send_report_email)
        self.start_date = self.get_start_date()
        self.end_date = self.get_end_date()
        self.athlete_names = self.ATHLETE_NAMES
        self.athletes = AthletesExtractor(
            athlete_names=self.athlete_names
        ).run()

        self.data = ActivitiesExtractor(
            start_date=self.start_date,
            end_date=self.end_date,
            athlete_names=self.athlete_names
        ).run()

    def get_start_date(self) -> datetime.datetime:
        return pd.to_datetime(self.base_variables.run_date - relativedelta(days=7))

    def get_end_date(self) -> datetime.datetime:
        return pd.to_datetime(self.base_variables.run_date)

    def generate_report(self) -> pd.DataFrame:
        self.logger.info(f"Generating report between {self.start_date} and {self.end_date} ")
        pass
