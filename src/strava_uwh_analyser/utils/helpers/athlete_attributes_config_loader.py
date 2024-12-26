from pathlib import Path
from typing import List
import yaml


class AthleteAttributesConfigLoader:

    ATHLETE_CONFIG_PATH = Path(__file__).parents[4] / "local_data/athlete_configs/athlete_attributes_config.yaml"

    def __init__(self):
        self.athlete_attributes_config = self.load_config()

    def load_config(self):
        with open(self.ATHLETE_CONFIG_PATH) as f:
            athlete_attributes_config = yaml.safe_load(f)
        return athlete_attributes_config

    def get_athletes_attribute_dict(self, athlete_names: List[str]) -> dict:
        return {
            athlete_name: self.athlete_attributes_config[athlete_name]
            for athlete_name in athlete_names
        }
