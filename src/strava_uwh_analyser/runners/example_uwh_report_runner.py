from strava_uwh_analyser.reports.example_uwh_report import ExampleReport


class ExampleUWHReportRunner:
    """Class to run the example report you should replace with your own report runner"""

    @classmethod
    def run(cls):
        ExampleReport(
            save_locally=True,
            send_report_email=True
        ).run()
