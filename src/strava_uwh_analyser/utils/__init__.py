import argparse
import datetime
import logging

from strava_uwh_analyser.utils.helpers.strava_handler import StravaHandler
from strava_uwh_analyser.utils.helpers.helper_functions import get_logging_level


def _2date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Parameters for process")
    parser.add_argument(
        "--environment",
        help="Environment you want to run process in",
        default="dev",
        choices=["tests", "prod", "dev"]
    )
    parser.add_argument(
        "--run-date",
        dest="run_date",
        help="The date you want to run the report for",
        default=datetime.date.today(),
        type=_2date
    )

    args, _ = parser.parse_known_args()

    if args.environment == "prod":
        args.logging_level = "info"
    elif args.environment == "tests":
        args.logging_level = "info"
    else:
        args.logging_level = "debug"

    return args


parsed_args = parse_args()


logging.basicConfig(
        level=get_logging_level(logging_level=parsed_args.logging_level),  # Set the minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Format of log messages
)

STRAVA_HANDLER = StravaHandler()

__all__ = ["parsed_args", "STRAVA_HANDLER"]
