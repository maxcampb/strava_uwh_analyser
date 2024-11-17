
# Strava UWH Analyser

This package allows users to upload Strava activities and analyse them for underwater hockey (UWH) specific metrics. 


# Setup to run locally

On windows, you can set the environment variable by running the following command in the terminal:
```bash
set ATHLETE_CREDENTIALS_PATH "C:\Users\maxca\Documents\GitHubProjects\strava_uwh_analyser\local_data\athlete_credentials.json"
```

On linux/mac, you can set the environment variable by running the following command in the terminal:
```bash
export ATHLETE_CREDENTIALS_PATH="/Users/maxca/Documents/GitHubProjects/strava_uwh_analyser/local_data/athlete_credentials.json"
```

# How to add a new report

1. Copy the report template
2. Setup the report to run the processes and format them
3. Create a report runner
4. Add a function that runs your runner in main
5. Add to console_scripts in you setup.py

# New athlete credentials

Run the following steps

```python

from strava_uwh_analyser.utils.helpers.strava_handler import StravaHandler

# Generate an authorization URL, send this link to athlete, and get them to extract code from URL after they sign in.
# Where URL takes form "http://localhost:8282/authorized?state=&code=XXXXXXXXXXXXXXXXXX&scope=read,activity:read"
StravaHandler.get_authorization_url()

# Retrieve their credentials 
StravaHandler.get_token_response("XXXXXXXXXXXXXXXXXX") 

```

