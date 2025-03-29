import datetime

import pandas as pd
import requests
import os
from typing import Dict, Optional
import json
import io
from dotenv import load_dotenv

from strava_uwh_analyser.utils.helpers.helper_functions import add_logger

load_dotenv()


@add_logger
class EmailSender:
    MAILGUN_API_URL = os.environ.get("MAILGUN_API_URL")
    MAILGUN_API_KEY = os.environ.get("MAILGUN_API_KEY")
    MAILGUN_SENDER_ADDRESS = os.environ.get("MAILGUN_SENDER_ADDRESS")

    def __init__(
            self,
            report_data: pd.DataFrame,
            report_name: str,
            to_addresses: Dict[str, str],
            date: Optional[datetime.date] = None
    ):
        self.report_name = report_name
        self.report_data = report_data
        assert to_addresses is not None
        self.to_addresses = to_addresses
        self.date = date
        if self.date is None:
            self.date = datetime.date.today()

    @staticmethod
    def format_report_data_as_bytes(data: pd.DataFrame) -> bytes:
        buffer = io.BytesIO()
        data.to_csv(buffer, index=False)
        buffer.seek(0)
        return buffer.read()

    def generate_email_body(self) -> str:
        return (
            f"Attached is the {self.report_name} report for run_date {self.date}"
        )

    def send_email(self) -> None:
        resp = requests.post(
            self.MAILGUN_API_URL,
            auth=("api", self.MAILGUN_API_KEY),
            files={"attachment":  (
                f"{self.report_name}_{self.date}.csv",
                self.format_report_data_as_bytes(self.report_data)
            )},
            data={
                "from": f" mailgun sender <{self.MAILGUN_SENDER_ADDRESS}>",
                "to": list(self.to_addresses.values()),
                "subject": f"{self.report_name} Report",
                "text": self.generate_email_body(),
            }
        )
        self.logger.info(f"Email sent with status code {resp.status_code}")
