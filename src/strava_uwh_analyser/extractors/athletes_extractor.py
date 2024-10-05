from typing import Optional, List, Dict
from stravalib.model import DetailedAthlete

from strava_uwh_analyser.utils.base_classes import StravaExtractor
from strava_uwh_analyser.utils.athlete_data import AthleteMaxHeartRates
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


class ProcessedAthlete:

    def __init__(
        self,
        athlete_name: str,
        athlete_id: str,
        athlete_details: DetailedAthlete,
        max_heart_rate: Optional[float] = None,
    ):
        self.athlete_name = athlete_name
        self.athlete_id = athlete_id
        self.athlete_details = athlete_details
        if max_heart_rate is None:
            self.max_heart_rate = AthleteMaxHeartRates[athlete_name.upper()].value
        else:
            self.max_heart_rate = max_heart_rate


@add_logger
class AthletesExtractor(StravaExtractor):

    def __init__(
            self,
            athlete_names: Optional[List[str]] = None,
    ):
        self.client = None
        self.athlete_names = self.get_athletes_names(athlete_names=athlete_names)

    def get_athletes_names(self, athlete_names) -> list:
        if athlete_names is None:
            athlete_names = [
                athlete_name
                for athlete_name, creds in self.strava_handler.credentials.items()
                if creds is not None
            ]

        return athlete_names

    def extract(self) -> Dict[str, list]:
        self.logger.debug("Extracting athletes")
        athletes = {}
        for athlete_name in self.athlete_names:
            self.client = self.strava_handler.get_configured_athlete_client(athlete_name)
            athletes.update({athlete_name: self.client.get_athlete()})

        return athletes

    def transform(self, data: Dict[str, list]) -> Dict[str, ProcessedAthlete]:
        self.logger.debug("Transforming athletes")
        athletes_data = {}
        for athlete_name, athlete in data.items():
            athletes_data[athlete_name] = (
                ProcessedAthlete(
                    athlete_name=athlete_name,
                    athlete_id=str(athlete.id),
                    athlete_details=athlete,
                    max_heart_rate=athlete.max_heartrate
                )
            )

        return athletes_data