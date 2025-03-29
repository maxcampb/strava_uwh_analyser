from stravalib.client import Client
import time
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from copy import deepcopy
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


load_dotenv(Path.home() / ".env")


@add_logger
class StravaHandler:
    STRAVA_CLIENT_ID = os.environ.get("STRAVA_CLIENT_ID")
    STRAVA_CLIENT_SECRET = os.environ.get("STRAVA_CLIENT_SECRET")
    CREDENTIALS = os.environ.get("ATHLETES_CREDENTIALS")
    client = Client()

    def __init__(self):
        self.credentials = json.loads(self.CREDENTIALS)
        self.update_credentials()

    def update_credentials(self):
        self.logger.info("Updating credentials ...")
        print(self.credentials)
        self.logger.info(self.credentials)
        if isinstance(self.credentials, str):
            self.credentials = json.loads(self.credentials)
        for athlete_name, athlete_credentials in self.credentials.items():
            if athlete_credentials is not None:
                if time.time() > athlete_credentials["expires_at"]:
                    refresh_response = self.client.refresh_access_token(
                        client_id=self.STRAVA_CLIENT_ID,
                        client_secret=self.STRAVA_CLIENT_SECRET,
                        refresh_token=athlete_credentials["refresh_token"]
                    )
                    access_token = refresh_response["access_token"]
                    refresh_token = refresh_response["refresh_token"]
                    expires_at = refresh_response["expires_at"]
                    self.credentials[athlete_name] = {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "expires_at": expires_at
                    }

    @classmethod
    def get_authorization_url(cls):
        return cls.client.authorization_url(
            client_id=cls.STRAVA_CLIENT_ID,
            redirect_uri="http://localhost:8282/authorized"
        )

    @classmethod
    def get_token_response(cls, code):
        return cls.client.exchange_code_for_token(
            client_id=cls.STRAVA_CLIENT_ID,
            client_secret=cls.STRAVA_CLIENT_SECRET,
            code=code
        )

    def get_configured_athlete_client(self, athlete_name: str):
        self.logger.info(f"Creating strava client for athlete {athlete_name} ...")
        client = deepcopy(self.client)
        athlete_credentials = self.credentials[athlete_name]
        client.access_token = athlete_credentials["access_token"]
        client.refresh_token = athlete_credentials["refresh_token"]
        client.token_expires_at = athlete_credentials["expires_at"]
        self.logger.info(f"Creating client was successful")

        return client


if __name__ == "__main__":
    StravaHandler.get_authorization_url()
    StravaHandler.get_token_response("XXXXXXXXXXXXXXXXXX")
    # URL Looks like this.
    # "http://localhost:8282/authorized?state=&code=XXXXXXXXXXXXXXXXXX&scope=read,activity:read"
