import abc
from typing import Union, Dict, Optional
from pathlib import Path
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
    report_name = None
    DATA_DIRECTORY = Path(__file__).parents[3] / "local_data/report_data"
    EMAIL_RECIPIENTS: Optional[Dict[str, str]] = None

    def __init__(
        self,
        save_locally,
        send_report_email,
    ):
        self.save_locally = save_locally
        self.send_report_email = send_report_email
        if send_report_email:
            if self.EMAIL_RECIPIENTS is None:
                raise ValueError(
                    "EMAIL_RECIPIENTS must be defined as the report class attribute if send_report_email is True"
                )

    @abc.abstractmethod
    def generate_report(self) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
        pass

    @property
    def report_file_name(self):
        return self.DATA_DIRECTORY / f"{self.report_name}_{self.base_variables.run_date}_report.csv"

    def save_report_locally(self, report_outputs: Union[pd.DataFrame, Dict[str, pd.DataFrame]]):
        if isinstance(report_outputs, dict):
            for output_name, output in report_outputs.items():
                output.to_csv(self.DATA_DIRECTORY / f"{output_name}_{self.base_variables.run_date}_report.csv")
        elif isinstance(report_outputs, pd.DataFrame):
            report_outputs.to_csv(self.report_file_name)
        else:
            raise ValueError("report_outputs must be a pandas DataFrame or a dictionary")

    def run(self):
        report = self.generate_report()
        if self.save_locally:
            self.save_report_locally(report_outputs=report)
        if self.send_report_email:
            EmailSender(report_data=report).send_email()
