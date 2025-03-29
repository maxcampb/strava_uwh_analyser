from typing import Optional, List, Dict
from stravalib.model import DetailedAthlete

from strava_uwh_analyser.utils.base_classes import StravaExtractor
from strava_uwh_analyser.utils.helpers.athlete_attributes_config_loader import AthleteAttributesConfigLoader
from strava_uwh_analyser.utils.helpers.helper_functions import add_logger


class ProcessedAthlete:
    PRIMARY_CONFIG_FIELDS = ["max_heart_rate"]

    def __init__(
        self,
        athlete_name: str,
        athlete_id: str,
        athlete_details: DetailedAthlete,
        athlete_configs: Optional[dict] = None,
    ):
        self.athlete_name = athlete_name
        self.athlete_id = athlete_id
        self.athlete_details = athlete_details
        self._process_athlete_configs(athlete_configs=athlete_configs)

    def _process_athlete_configs(self, athlete_configs: Optional[dict]):
        self.athlete_configs = athlete_configs
        for field in self.PRIMARY_CONFIG_FIELDS:
            try:
                setattr(self, field, self.athlete_configs[field])
            except KeyError:
                setattr(self, field, None)


@add_logger
class AthletesExtractor(StravaExtractor):

    def __init__(
            self,
            athlete_names: Optional[List[str]] = None,
            load_athlete_configs: bool = True
    ):
        self.client = None
        self.athlete_names = self.get_athletes_names(athlete_names=athlete_names)
        if load_athlete_configs:
            self.athlete_configs = AthleteAttributesConfigLoader().get_athletes_attribute_dict(athlete_names)
        else:
            self.athlete_configs = None

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
                    athlete_configs=self.athlete_configs[athlete_name] if self.athlete_configs is not None else None,
                )
            )

        return athletes_data
