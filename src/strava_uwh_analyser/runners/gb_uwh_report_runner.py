from strava_uwh_analyser.reports.gb_uwh_report import GBUWHReport


class GBUWHReportRunner:

    @classmethod
    def run(cls):
        GBUWHReport(
            send_report_email=True
        ).generate_report()
