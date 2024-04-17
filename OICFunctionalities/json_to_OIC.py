from OIC import createJSONFile
import requests
import json
import os

# Define the directory containing the JSON files
json_dir = "output"

# Iterate through each JSON file in the directory
for file in os.listdir(json_dir):
    if file.endswith(".json"):
        # Construct the full file path
        json_file_path = os.path.join(json_dir, file)
        print(json_file_path)
        # Create the JSON file
        createJSONFile(json_file_path)


