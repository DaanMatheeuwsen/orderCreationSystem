from getOrderId import getLastOrderId
from GetLocation import getGidLocation
import json
import os
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import requests


def createJSONFile(input_file_path, output_file_path):

    # Load content from the provided JSON file
    with open(input_file_path, "r") as json_file:
        json_data = json.load(json_file)

    print("Loaded JSON data:", json_data)

    next_order_id = getLastOrderId()

    order_information = {}
    loading_info = {}
    unloading_info = {}
    goods = {}
    truck = {}
    goods_information = {}

    # Extract relevant information from the JSON data
    for key, value in json_data.items():
        if key == "Booking number":
            order_information["Booking number"] = value["value"]
        elif key == "Agreed tariff":
            order_information["Agreed tariff"] = value["value"]
        elif key == "Invoice reference":
            order_information["Invoice reference"] = value["value"]
        # Add more conditions to extract other information as needed

    print(order_information)

    # Populate loading information
    loading_info["Name"] = json_data.get("Name (Loading)", {}).get("value", "").upper()
    loading_info["City"] = json_data.get("City (Loading)", {}).get("value", "").upper()
    loading_info["Postalcode"] = json_data.get("Loading Postalcode", {}).get("value", "")
    earlyPickupDate = json_data.get("Requested loading date from", {}).get("value", "")
    earlyPickupTime = json_data.get("Requested loading time", {}).get("value", "")
    loading_reference = json_data.get("Loading Reference", {}).get("value", "")
    earlyPickupFullDate = earlyPickupDate + "T" + earlyPickupTime + "+00:00"
    print (earlyPickupFullDate)
    # Populate unloading information
    unloading_info["Name"] = json_data.get("Name (Unloading)", {}).get("value", "").upper()
    unloading_info["City"] = json_data.get("City (Unloading)", {}).get("value", "").upper()
    unloading_info["Postalcode"] = json_data.get("Postalcode (Unloading)", {}).get("value", "")
    earlyDeliveryDate = json_data.get("Requested unloading date from", {}).get("value", "")
    earlyDeliveryTime = json_data.get("Requested unloading time", {}).get("value", "")
    unloading_reference = json_data.get("Unloading Reference", {}).get("value", "")
    earlyDeliveryFullDate = earlyDeliveryDate + "T" + earlyDeliveryTime + "+00:00"
    print(earlyDeliveryFullDate)

    # Populate goods information
    goods["Width"] = json_data.get("Width", {}).get("value", "")
    goods["Length"] = json_data.get("Length", {}).get("value", "")
    goods["Weight per ship unit"] = json_data.get("Weight per ship unit", {}).get("value", "")
    goods["Height"] = json_data.get("Height", {}).get("value", "")
    goods["Quantity"] = json_data.get("Quantity", {}).get("value", "")
    goods["Ship unit"] = json_data.get("Ship Unit", {}).get("value", "")

    # Populate truck information
    truck["Load/Unloading information"] = json_data.get("Load/Unloading Information", {}).get("value", "")
    truck["Palletexchange"] = json_data.get("Palletexchange", {}).get("value", "")
    truck["Licenseplate required"] = json_data.get("Licenseplate Required", {}).get("value", "")

    # Construct early pickup and delivery dates
    # empty_json_path = "empty_json_file.json"

    # Load content from the empty JSON file
    with open('./output/Order_Folder/empty_file.json', "r") as empty_file:
        empty_data = json.load(empty_file)

    # Update the empty_data dictionary with extracted information
    empty_data["destLocationGid"] = getGidLocation(unloading_info["City"], unloading_info["Postalcode"])
    empty_data["sourceLocationGid"] = getGidLocation(loading_info["City"], loading_info["Postalcode"])
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
            "orderReleaseRefnumValue": order_information["Booking number"]
        }
    ]
    empty_data["remarks"]["items"] = [
        {
            "remarkQualGid": "RSK.LOAD_UNLOADING_INFORMATION",
            "remarkText": truck["Load/Unloading information"]
        },
        {
            "remarkQualGid": "RSK.LICENSE_PLATE",
            "remarkText": truck["Licenseplate required"]
        },
        {
            "remarkQualGid": "RSK.PALLET_EXCHANGE",
            "remarkText": truck["Palletexchange"]
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
                    "value": goods["Width"],
                    "unit": "M"
                },
                "unitLength": {
                    "value": goods["Length"],
                    "unit": "M"
                },
                "attribute1": "",
                "shipUnitCount": goods["Quantity"],
                "unitWeight": {
                    "value": goods["Weight per ship unit"],
                    "unit": "KG"
                },
                "flexCommodityCode": "RSK." + goods["Ship unit"],
                "unitHeight": {
                    "value": goods["Height"],
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

    # Save the updated data to the output file
    with open(output_file_path, "w") as updated_file:
        json.dump(empty_data, updated_file, indent=4)
        print(json)

createJSONFile('./output/Order_Folder/test-order.json', './output/Order_Folder/empty_file.json')