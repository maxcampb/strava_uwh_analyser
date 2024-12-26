from typing import Optional, List, Dict
from stravalib.model import DetailedAthlete

from strava_uwh_analyser.utils.base_classes import StravaExtractor
from strava_uwh_analyser.utils.helpers.athlete_attributes_config_loader import AthleteAttributesConfigLoader
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


class ProcessedAthlete:

    def __init__(
        self,
        athlete_name: str,
        athlete_id: str,
        athlete_details: DetailedAthlete,
        athlete_attributes: Optional[dict] = None,
    ):
        self.athlete_name = athlete_name
        self.athlete_id = athlete_id
        self.athlete_details = athlete_details
        if athlete_attributes is not None:
            self.max_heart_rate = athlete_attributes.pop("max_heart_rate")
        self.athlete_attributes = athlete_attributes


@add_logger
class AthletesExtractor(StravaExtractor):

    athlete_attributes = {}

    def __init__(
            self,
            athlete_names: Optional[List[str]] = None,
            load_athlete_configs: bool = False,
    ):
        self.client = None
        self.athlete_names = self.get_athletes_names(athlete_names=athlete_names)
        if load_athlete_configs:
            self.athlete_attributes = (
                AthleteAttributesConfigLoader()
                .get_athletes_attribute_dict(athlete_names=athlete_names)
            )

    def get_athletes_names(self, athlete_names) -> list:
        if athlete_names is None:
            athlete_names = [
                athlete_name
                for athlete_name, creds in self.strava_handler.credentials.items()
                if creds is not None
            ]

        return athlete_names

    def extract(self) -> Dict[str, list]:
        self.logger.info("Extracting athletes")
        athletes = {}
        for athlete_name in self.athlete_names:
            self.client = self.strava_handler.get_configured_athlete_client(athlete_name)
            athletes.update({athlete_name: self.client.get_athlete()})

        return athletes

    def transform(self, data: Dict[str, list]) -> Dict[str, ProcessedAthlete]:
        self.logger.info("Transforming athletes")
        athletes_data = {}
        for athlete_name, athlete in data.items():
            athletes_data[athlete_name] = (
                ProcessedAthlete(
                    athlete_name=athlete_name,
                    athlete_id=str(athlete.id),
                    athlete_details=athlete,
                    athlete_attributes=self.athlete_attributes.get(athlete_name, None)
                )
            )

        return athletes_data
