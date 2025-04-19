
# Strava UWH Analyser

This package allows users to extract STRAVA activities, analyse them for underwater hockey (UWH) specific metrics, and then send them to coaches or players (e.g. via email). It follows an Extract-Transform-Load (ETL) structure.

Some general repository definitions:

* Extractors: used to extract data from a source (often from STRAVA)
* Processors: used to process data and return UWH specific metrics
* Reports: an class that contains the full infrastructure for running a report, including an orchestrator run method.
* Runners: Wrapper class which is designed to run a particular report.

 Contributions to repository are encouraged.

**WHEN MAKING CHANGES TO THIS REPO, do not commit directly to main branch. Instead commit to another branch and open a PR.**

# Setup to run locally

1. Setup a python interpreter running python version 3.10
2. Install invoke, piptools
    ```bash
    pip install invoke pip-tools
    ```
3. Install requirements
    ```bash
    invoke build
    ```
4. Install package using the setup.py
    ```bash
    pip install --editable .
    ```
### Notes

* Make sure that you have environment variables from gb_uwh_report\env.example available 
(e.g. through a .env file or defined).
* Make sure that you have the credentials for all the athletes specified in your report. 
Where, ATHLETES_CREDENTIALS should be specified as a JSON str in your .env, for examples:

```text
ATHLETES_CREDENTIALS="{\"max_campbell\": {\"access_token\": \"ahshw892303\", \"refresh_token\": \"osiw9o223os9\", \"expires_at\": 173375}, \"james_smith\": {\"access_token\": \"ahshw892303\", \"refresh_token\": \"osiw9o223os9\", \"expires_at\": 173375}}\"
```
If you are missing athlete credentials just change the list of athletes instanced in your report.

# How to add a new report

1. Copy the report template
2. Setup the report to run the processes and format them
3. Create a report runner
4. Add a function that runs your runner in main
5. Add to console_scripts in you setup.py

# Add new athlete to the report

You need to do three things to add a new athlete.

1. Add their name to the report you with to add them to (e.g. ```src/strava_uwh_analyser/reports/example_uwh_report.py```)

2. Add there athlete configs/metadata to ```src/strava_uwh_analyser/configs/athlete_attributes_config.yaml```

3. Get new athlete to authenticate the usage of their strava data in the application, retrieve their access keys, and 
add them to your ATHLETES_CREDENTIALS.

To do this, run the following steps

```python

from strava_uwh_analyser.utils.helpers.strava_handler import StravaHandler

# Generate an authorization URL, send this link to athlete, and get them to send you URL so you can extract the 
# the access code from URL after they sign in (not the link will seem broken but code is in URL).
# Where URL takes form "http://localhost:8282/authorized?state=&code=XXXXXXXXXXXXXXXXXX&scope=read,activity:read"
StravaHandler.get_authorization_url()

# Retrieve their credentials 
StravaHandler.get_token_response("XXXXXXXXXXXXXXXXXX") 

```
Then you need to add this dictionary properly formatted to your ATHLETES_CREDENTIALS json string
