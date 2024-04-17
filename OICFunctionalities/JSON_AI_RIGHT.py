import json
from fuzzywuzzy import process, fuzz

# Define the standard values
standard_values = [
    "Booking number",
    "Agreed tariff",
    "Invoice reference",
    "Company name",
    "Contact person",
    "E-mail address",
    "Phone Number",
    "Loading address",
    "Loading date",
    "Loading Postalcode",
    "Loading reference",
    "Unloading address",
    "Unloading date",
    "Unloading Postalcode",
    "Unloading reference",
    "Quantity",
    "Ship unit",
    "Weight per ship unit",
    "Total weight",
    "Length",
    "Width",
    "Height",
    "Stackable",
    "Description",
    "Pallet exchange",
    "ADR",
    "ADR code",
    "A-sign / waste registration",
    "Safety equipment",
    "Insurance next to CMR conditions",
    "Temperature",
    "Minimum Temperature",
    "Maximum temperature",
    "Trailer type",
    "Load/Unloading information",
    "License plate required",
    "Remark"
]

# Function to match values with standard values using fuzzy matching
def match_values(order, standard_values):
    matched_values = {}
    unknown_count = 0
    for standard_value in standard_values:
        matched_company_value, similarity = process.extractOne(standard_value, order.keys())
        if similarity >= 80:  # Adjust similarity threshold as needed
            matched_values[standard_value] = {
                "company_phrasing": matched_company_value,
                "value": order[matched_company_value],
                "similarity": similarity
            }
        else:
            unknown_count += 1
            matched_values[f"Unknown_value_{unknown_count}"] = {
                "company_phrasing": matched_company_value,
                "value": order[matched_company_value],
                "similarity": similarity
            }
    return matched_values

# Read dataset from JSON file
json_file_path = './output/Order_Folder/Multiple-orders.json'
with open(json_file_path, 'r') as file:
    dataset = json.load(file)

# Format properties using default values
formatted_properties = match_values(dataset, standard_values)

# Write the formatted properties to the new JSON file
with open(json_file_path, 'w') as file:
    json.dump(formatted_properties, file, indent=2)
