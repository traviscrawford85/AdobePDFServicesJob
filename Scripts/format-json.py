import json

# Corrected file path using a raw string
file_path = r"output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json"

# Load and pretty-print the JSON
with open(file_path, "r") as file:
    data = json.load(file)
    print(json.dumps(data, indent=4))
