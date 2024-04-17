import requests
from datetime import datetime

# API endpoint
api_url = "https://otmgtm-test-rooskensgroupcloud.otmgtm.eu-frankfurt-1.ocs.oraclecloud.com/logisticsRestApi/resources-int/v2/orderReleases"

# OTM API credentials
username = "RSK.INTEGRATION"
password = "Netherlands@2024"

def getLastOrderId():
    current_date = datetime.now().strftime('%Y%m%d')
    prefix = "INT"

    # Construct the query parameters
    query_param = f"q=orderReleaseXid co \"{prefix}-{current_date}\""

    # Construct the full URL
    full_url = f"{api_url}?{query_param}"

    # Send GET request
    response = requests.get(full_url, auth=(username, password))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_data = response.json()
        # Extract the orderReleaseXid values
        order_ids = [item["orderReleaseXid"] for item in json_data['items']]
        print("All order IDs:", order_ids)
        # Extract the numeric part of the orderReleaseXid and convert them to integers
        numeric_ids = [int(order_id.split("-")[2]) for order_id in order_ids if order_id.startswith(prefix)]
        print("Numeric IDs:", numeric_ids)
        # Find the highest numeric ID
        highest_number = max(numeric_ids) if numeric_ids else 0
        print("Highest numeric ID:", highest_number)
        # Generate the next orderReleaseXid
        next_order_release_id = f"{prefix}-{current_date}-{highest_number + 1:04d}"
        print("Next orderReleaseXid:", next_order_release_id)
        return next_order_release_id
    else:
        # If the request was not successful, raise an exception with the error information
        raise Exception(f"Error: {response.status_code}, Error Content: {response.content}")

getLastOrderId()

