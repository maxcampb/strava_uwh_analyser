import pytest

from strava_uwh_analyser.extractors.activities_extractor import ActivitiesExtractor, ProcessedActivityData
from strava_uwh_analyser.extractors.athletes_extractor import AthletesExtractor, ProcessedAthlete
from strava_uwh_analyser.utils.helpers.athlete_attributes_config_loader import AthleteAttributesConfigLoader


@pytest.fixture
def athlete_names():
    return ["max_campbell"]


@pytest.fixture
def start_date():
    return "2025-01-01"


@pytest.fixture
def end_date():
    return "2025-01-31"


def test_activities_extractor(athlete_names, start_date, end_date):
    activities_extractor = ActivitiesExtractor(
        start_date=start_date,
        end_date=end_date,
        athlete_names=athlete_names,
    )
    activities = activities_extractor.run()
    assert len(activities) > 0
    for activities in activities:
        assert isinstance(activities, ProcessedActivityData)


def test_athletes_extractor(athlete_names):
    athletes_extractor = AthletesExtractor(
        athlete_names=athlete_names,
        load_athlete_configs=False,
    )
    athletes = athletes_extractor.run()
    assert len(athletes) == len(athlete_names)
    for athlete in athletes.values():
        assert isinstance(athlete, ProcessedAthlete)


def test_athlete_attributes_config_loader(athlete_names):
    athlete_attributes_config_loader = AthleteAttributesConfigLoader()
    athlete_attributes_config = (
        athlete_attributes_config_loader.get_athletes_attribute_dict(athlete_names=athlete_names)
    )
    assert isinstance(athlete_attributes_config, dict)
    assert len(athlete_attributes_config) > 0
