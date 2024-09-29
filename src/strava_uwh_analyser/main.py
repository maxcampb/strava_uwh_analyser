from __future__ import print_function
import time
import swagger_client
from swagger_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: strava_oauth
swagger_client.configuration.access_token =

# create an instance of the API class
api_instance = swagger_client.APIHealthApi()
id = 789 # Long | The identifier of the activity.
includeAllEfforts = True # Boolean | To include all segments efforts. (optional)

try:
    # Get Activity
    api_response = api_instance.g_et_system_health_api_volume_summary(id, includeAllEfforts=includeAllEfforts)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ActivitiesApi->getActivityById: %s\n" % e)