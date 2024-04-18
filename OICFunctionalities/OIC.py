from getOrderId import getLastOrderId
from GetLocation import getGidLocation
import json
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests

# API endpoint
api_url = "https://rsk-dev-oic-frkpvjuqpmjx-fr.integration.ocp.oraclecloud.com:443/ic/api/integration/v1/flows/rest/OTMCONVERSION_2/1.0/orderFields"

# OTM API credentials
username = "Daan.matheeuwsen@rooskensgroup.com"
password = "Svbudel2018-"

def createJSONFile(output_file_path):
    def fuzzy_match(name, options, threshold=30):
        """
        Perform fuzzy matching to find the best match for a given name from a list of options.
        """
        # Create a list of tuples containing the option and its similarity score with the name
        matches = [(option, fuzz.partial_ratio(name, option)) for option in options]
        
        # Filter matches based on the threshold
        filtered_matches = [(option, score) for option, score in matches if score >= threshold]
        
        # Sort filtered matches by similarity score in descending order
        sorted_matches = sorted(filtered_matches, key=lambda x: x[1], reverse=True)
        
        # Return the best match if any
        if sorted_matches:
            return sorted_matches[0][0]  # Return the name of the best match
        else:
            return None  # Return None if no match is found

    next_order_id = getLastOrderId()

    # Check if the converted_data.json file exists and is non-empty
    if os.path.exists(output_file_path) and os.path.getsize(output_file_path) > 0:
        # Load content from the converted_data.json file
        with open(output_file_path, "r") as updated_file:
            filled_data = json.load(updated_file)

    order_information = filled_data.get('Order Information', [{}])[0]
    booking_number = order_information.get('Booking number', '')  # Get the postal code from loading information

    loading_info = filled_data.get('Loading information', [{}])[0]  # Get the first item in the list or an empty dictionary
    loading_name = loading_info.get('Name', '').upper()  # Get the name from loading information
    loading_city = loading_info.get('City', '').upper()  # Get the city from loading information
    loading_postal_code = loading_info.get('Postalcode', '')  # Get the postal code from loading information
    earlyPickupDate = loading_info.get('Requested loading date from', '')
    earlyPickupTime = loading_info.get('Requested loading time', '')
    loading_reference = loading_info.get('Loading reference', '')
    earlyPickupFullDate = (earlyPickupDate + "T" + earlyPickupTime + "+00:00")
    
    loadingLocationId = getGidLocation(loading_city, loading_postal_code)

    best_match_loading = fuzzy_match(loading_name, loadingLocationId)

    unloading_info = filled_data.get('Unloading Information', [{}])[0]  # Get the first item in the list or an empty dictionary
    unloading_name = unloading_info.get('Name', '').upper()  # Get the name from unloading information
    unloading_city = unloading_info.get('City', '').upper()  # Get the city from unloading information
    unloading_postal_code = unloading_info.get('Postalcode', '')  # Get the postal code from unloading information
    earlyDeliveryDate = unloading_info.get('Requested unloading date from', '')
    earlyDeliveryTime = unloading_info.get('Requested unloading time', '')
    unloading_reference = unloading_info.get('Unloading reference', '')
    earlyDeliveryFullDate = (earlyDeliveryDate + "T" + earlyDeliveryTime + "+00:00")

    unloadingLocationId = getGidLocation(unloading_city, unloading_postal_code)

    best_match_unloading = fuzzy_match(unloading_name, unloadingLocationId)

    goods = filled_data.get('Goods', [{}])[0]
    unitWidth = goods.get('Width', '')
    unitLength = goods.get('Length', '')
    unitWeight = goods.get('Weight per ship unit', '')
    unitHeight = goods.get('Height', '')
    shipUnitcount = goods.get('Quantity')
    shipUnit = goods.get('Ship unit', '')


    truck = filled_data.get('Truck', [{}])[0]
    goods_information = filled_data.get('Goods-Information', [{}])[0]
    loading_information = truck.get('Load/Unloading information', '')  # Get the postal code from loading information
    palletExchange = goods_information.get('Palletexchange', '')  # Get the postal code from loading information
    licensePlate_required = truck.get('Licenseplate required', '')  # Get the postal code from loading information
    print(palletExchange)

    empty_json_path = "empty_json_file.json"

    # Load content from the empty JSON file
    with open("empty_json_file.json", "r") as empty_file:
        empty_data = json.load(empty_file)

    # Update the destLocationGid, sourceLocationGid, and orderReleaseXid
    empty_data["destLocationGid"] = best_match_unloading
    empty_data["sourceLocationGid"] = best_match_loading
    empty_data["orderReleaseXid"] = next_order_id
    empty_data["earlyDeliveryDate"]["value"] = earlyDeliveryFullDate
    empty_data["earlyPickupDate"]["value"] = earlyPickupFullDate
    empty_data["refnums"]["items"] = [
        {
            "orderReleaseRefnumQualGid": "RSK.LOADING_REFERENCE",
            "orderReleaseRefnumValue": loading_reference
        },
        {
            "orderReleaseRefnumQualGid": "RSK.UNLOADING_REFERENCE",
            "orderReleaseRefnumValue": unloading_reference
        },
        {
            "orderReleaseRefnumQualGid": "RSK.CUST ORDER NUMBER",
            "orderReleaseRefnumValue": booking_number
        }
    ]
    empty_data["remarks"]["items"] = [
        {
            "remarkQualGid": "RSK.LOAD_UNLOADING_INFORMATION",
            "remarkText":  loading_information
        },
        {
            "remarkQualGid": "RSK.LICENSE_PLATE",
            "remarkText": licensePlate_required
        },
        {
            "remarkQualGid": "RSK.PALLET_EXCHANGE",
            "remarkText": palletExchange
        }
    ]
    empty_data["invParties"]["items"] = [
        {
            "involvedPartyQualGid": "BILL-TO",
            "involvedPartyContactGid": "RSK.50187"
        },
        {
            "involvedPartyQualGid": "RSK.CUSTOMER-OPS",
            "involvedPartyContactGid": "RSK.DAAN-MATHEEUWSEN"
        }
    ]
    empty_data["shipUnits"] = {
        "items": [
            {
                "shipUnitXid": next_order_id + "-0001",
                "transportHandlingUnitGid": "RSK.FTL",
                "unitWidth": {
                    "value": unitWidth,
                    "unit": "M"
                },
                "unitLength": {
                    "value": unitLength,
                    "unit": "M"
                },
                "attribute1": "",
                "shipUnitCount": shipUnitcount,
                "unitWeight": {
                    "value": unitWeight,
                    "unit": "KG"
                },
                "flexCommodityCode": "RSK." + shipUnit,
                "unitHeight": {
                    "value": unitHeight,
                    "unit": "M"
                },
                "lines": {
                    "items": [
                        {
                            "shipUnitLineNo": 1,
                            "orderReleaseLineGid": "RSK.160035"
                        }
                    ]
                }
            }
        ]
    }


    # Save the updated data back to the file
    with open("empty_json_file.json", "w") as updated_file:
        json.dump(empty_data, updated_file, indent=4)


    sendJSONDataToOIC("empty_json_file.json")


def sendJSONDataToOIC(json_file_path):
    # Load the JSON data from the file
    with open(json_file_path, "r") as json_file:
        json_data = json.load(json_file)

    # Send POST request with Basic authentication
    response = requests.post(api_url, json=json_data, auth=(username, password))

    # Check if the request was successful
    if response.status_code == 200:
        print(f"API call for {json_file_path} successful.")
        # Optionally, print the response content
        print("Response:", response.json())
    else:
        print(f"Error for {json_file_path}:", response.status_code)
        # Print the error response content
        print("Error Content:", response.content)