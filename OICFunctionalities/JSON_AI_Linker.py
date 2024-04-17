import json
from fuzzywuzzy import process, fuzz
import spacy
import torch

# Load spaCy models for German, Dutch, and English
nlp_german = spacy.load("de_core_news_lg")
nlp_dutch = spacy.load("nl_core_news_lg")
nlp_english = spacy.load("en_core_web_lg")

# Define standard values for comparison
standard_values = {
    "Order Information": {
        "Booking number": "Booking number",
        "Agreed tariff": "Agreed tariff",
        "Invoice reference": "Invoice reference"
    },
    "Contact Information BILL-TO": {
        "Company name (Invoice company)": "Company name",
        "Contact person name": "Contact person name",
        "E-mail address": "E-mail address",
        "Phone Number": "Phone Number"
    },
    "Loading Information": {
        "loading address": "loading address",
        "Loading date": "Loading date",
        "Loading Postalcode": "Loading Postalcode",
        "Loading reference": "Loading reference"
    },
    "Unloading Information": {
        "Unloading address": "Unloading address",
        "Unloading date": "Unloading date",
        "Unloading Postalcode": "Unloading Postalcode",
        "Unloading reference": "Unloading reference"
    },
    "Goods": {
        "Quantity": "Quantity",
        "Ship unit": "Ship unit",
        "Weight per ship unit": "Weight per ship unit",
        "Total weight": "Total weight",
        "Length": "Length",
        "Width": "Width",
        "Height": "Height",
        "Stackable": "Stackable",
        "Description": "Description"
    },
    "Goods-Information": {
        "Pallet exchange": "Pallet exchange",
        "ADR": "ADR",
        "ADR code": "ADR code",
        "A-sign / waste registration": "A-sign / waste registration",
        "Safety equipment": "Safety equipment",
        "Insurance next to CMR conditions": "Insurance next to CMR conditions",
        "Temperature": "Temperature",
        "Minimum Temperature": "Minimum Temperature",
        "Maximum temperature": "Maximum temperature"
    },
    "Truck": {
        "Trailer type": "Trailer type",
        "Load/Unloading information": "Load/Unloading information",
        "License plate required": "License plate required",
        "Remark": "Remark"
    }
}

def map_equivalent_fields(field, standard_values):
    best_match = None
    best_similarity = 0
    matched_property = None
    for section_name, section_properties in standard_values.items():
        for standard_key, standard_value in section_properties.items():
            similarity = fuzz.partial_ratio(field, standard_key)
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = section_name
                matched_property = standard_value
    if best_similarity >= 30:  
        return best_match, matched_property, best_similarity
    else:
        return None, None, None

def format_properties(dataset, standard_values):
    formatted_properties = {
        "Order Information": {},
        "Contact Information BILL-TO": {},
        "Loading Information": {},
        "Unloading Information": {},
        "Goods": {},
        "Goods-Information": {},
        "Truck": {}
    }

    linked_properties = set()  # Keep track of already linked properties

    # Iterate through the dataset
    for section, entries in dataset.items():
        for entry in entries:
            # Check which section the property belongs to and add it to the appropriate dictionary
            for key, value in entry.items():
                # Find the best matching section name and property
                matched_section, matched_property, similarity = map_equivalent_fields(key, standard_values)
                if matched_section and matched_property and matched_property not in linked_properties:
                    formatted_properties[matched_section][key] = {
                        "linked_property": matched_property,
                        "linked_value": value,
                        "similarity": similarity
                    }
                    linked_properties.add(matched_property)  # Add linked property to the set

    # Include entries for properties that were not linked
    for section, standard_props in standard_values.items():
        for prop_key, prop_value in standard_props.items():
            if prop_value not in linked_properties:
                formatted_properties[section][prop_key] = {
                    "linked_property": "none",
                    "linked_value": value,
                    "similarity": 0
                }

    return formatted_properties



# Read dataset from JSON file
json_file_path = './output/Order_Folder/Multiple-orders.json'
with open(json_file_path, 'r') as file:
    dataset = json.load(file)

# Format properties using default values
formatted_properties = format_properties(dataset, standard_values)

# Print formatted properties for each section
for section, properties in formatted_properties.items():
    print(f"{section}:")
    for key, value in properties.items():
        print(f"  '{key}': '{value}'")

# Write the formatted properties to the new JSON file
with open(json_file_path, 'w') as file:
    json.dump(formatted_properties, file, indent=2)
