from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename  # Import secure_filename function
import pandas as pd
import json
import os
import subprocess


app = Flask(__name__)
CORS(app)

def convert_time_format(time_str):
    # Check if the value is an integer
    if isinstance(time_str, int):
        # Convert integer to HH:MM:SS format
        hours = str(time_str // 100).zfill(2)
        minutes = str(time_str % 100).zfill(2)
        return f"{hours}:{minutes}:00"
    # Check if the value is not null and is a string
    elif pd.notnull(time_str) and isinstance(time_str, str):
        # Convert ##:## format to HH:MM:SS
        parts = time_str.split(':')
        return f"{parts[0]}:{parts[1]}:00"
    else:
        return time_str

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_files = request.files.getlist('files')
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)

    for file in uploaded_files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(output_dir, filename)
        file.save(file_path)

        excel_data = pd.read_excel(file_path, sheet_name=None)
        has_rsk_template = False
        all_excel_data = {}

        for sheet_name, sheet_data in excel_data.items():
            if 'RSK_Template' in sheet_data.columns:
                has_rsk_template = True

            if isinstance(sheet_data, pd.DataFrame):  
                sheet_data = sheet_data.applymap(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x)
            elif isinstance(sheet_data, pd.Series): 
                sheet_data = sheet_data.apply(lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x)
            if 'Requested loading time' in sheet_data:
                sheet_data['Requested loading time'] = sheet_data['Requested loading time'].apply(convert_time_format)
            if 'Requested unloading time' in sheet_data:
                sheet_data['Requested unloading time'] = sheet_data['Requested unloading time'].apply(convert_time_format)

            all_excel_data[sheet_name] = sheet_data.to_dict(orient='records')

        json_file_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}.json")
        with open(json_file_path, "w") as json_file:
            json.dump(all_excel_data, json_file, indent=2)

        if has_rsk_template:
            output_subdir = os.path.join(output_dir, 'RSK_Template_Folder')
        else:
            output_subdir = os.path.join(output_dir, 'Order_Folder')
        os.makedirs(output_subdir, exist_ok=True)

        # Move the JSON file to the appropriate folder
        os.replace(json_file_path, os.path.join(output_subdir, f"{os.path.splitext(filename)[0]}.json"))

    return 'Conversion complete.', 200

@app.route('/saveJson', methods=['POST'])
def save_json():
    try:
        json_data = request.get_json()  # Get the JSON data from the request
        with open('./output/Order_Folder/Multiple-orders.json', 'w') as json_file:
            json_file.write(json.dumps(json_data, indent=2))  # Write the JSON data to the file
        print('JSON file updated successfully')
        return jsonify({'message': 'JSON file updated successfully'}), 200
    except Exception as e:
        print('Error writing JSON file:', e)
        return jsonify({'error': 'Error writing JSON file'}), 500

@app.route('/send_to_OTM', methods=['POST'])
def send_to_OTM():
    # Call the json_to_OIC.py script
    subprocess.run(['python', './OICFunctionalities/json_to_OIC.py'])
    return 'Data sent to OTM.', 200

if __name__ == '__main__':
    app.run(debug=True)
