import requests

# API endpoint
api_url = "https://otmgtm-test-rooskensgroupcloud.otmgtm.eu-frankfurt-1.ocs.oraclecloud.com/logisticsRestApi/resources-int/v2/locations"

# OTM API credentials
username = "RSK.INTEGRATION"
password = "Netherlands@2024"

def getGidLocation(cityName, postalCode):
    # Construct the query parameters
    query_param = f"q=locationXid co \"{cityName}\" AND postalCode co \"{postalCode}\""

    # Construct the full URL
    full_url = f"{api_url}?{query_param}"

    # Send GET request
    response = requests.get(full_url, auth=(username, password))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        json_data = response.json()
        # Extract and return the locationXid values as a list
        location_ids = ["RSK." + item.get("locationXid") for item in json_data['items']]
        return location_ids
    else:
        print("Error:", response.status_code)
        # Print the error response content
        print("Error Content:", response.content)
        # Return an empty list if there's an error
        return []
