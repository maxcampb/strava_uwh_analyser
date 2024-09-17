import argparse
import logging


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(description="Parameters for process")
    parser.add_argument(
        "--environment",
        help="Environment you want to run process in",
        default="dev",
        choices=["tests", "prod", "dev"]
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


def set_logging_level(
        logger: logging.Logger,
        logging_level: parsed_args.logging_level,
) -> None:
    if logging_level == "debug":
        logger.setLevel(logging.DEBUG)
    elif logging_level == "info":
        logger.setLevel(logging.INFO)
    else:
        f"Logging level {logging_level} is not implemented"


__all__ = ["parsed_args"]
