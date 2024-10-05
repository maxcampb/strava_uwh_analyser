import abc
from typing import Union
import pandas as pd
from strava_uwh_analyser.utils import *
from strava_uwh_analyser.utils.helpers.email_sender import EmailSender


class BaseVariables:
    arguments = parsed_args
    environment = parsed_args.environment
    logging_level = parsed_args.logging_level
    run_date = parsed_args.run_date


class StravaExtractor(abc.ABC):
    base_variables = BaseVariables()
    strava_handler = STRAVA_HANDLER
    logger = None

    @abc.abstractmethod
    def extract(self) -> Union[pd.DataFrame, dict]:
        pass

    @abc.abstractmethod
    def transform(self, data: Union[pd.DataFrame, dict]) -> pd.DataFrame:
        pass

    def run(self) -> pd.DataFrame:
        data = self.extract()
        data = self.transform(data)
        return data


class BaseReport(abc.ABC):
    base_variables = BaseVariables()

    def __init__(
        self,
        save_locally,
        send_report_email,
    ):
        self.save_locally = save_locally
        self.send_report_email = send_report_email

    @abc.abstractmethod
    def generate_report(self):
        pass

    def upload(self):
        pass

    def run(self):
        report = self.generate_report()
        if self.save_locally:
            self.upload()
        if self.send_report_email:
            EmailSender(report_data=report).send_email()
