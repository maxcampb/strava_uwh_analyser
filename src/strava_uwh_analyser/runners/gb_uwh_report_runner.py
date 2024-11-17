from strava_uwh_analyser.reports.gb_uwh_report import GBUWHReport


class GBUWHReportRunner:

    @classmethod
    def run(cls):
        GBUWHReport(
            save_locally=True,
            send_report_email=False
        ).run()
