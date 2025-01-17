import json

# Input structured JSON and PDF dimensions
structured_json_path = r"output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json"
adobe_json_path = r"output\Completed1040\adobe_edit_payload.json"

pdf_height = 792  # Letter size PDF height (example)
pdf_width = 612   # Letter size PDF width (example)

# Load structured JSON
with open(structured_json_path, "r") as file:
    structured_json = json.load(file)

# Prepare Adobe JSON
adobe_json = {"elements": []}

# Map structured JSON to Adobe JSON format
for element in structured_json["elements"]:
    path = element.get("Path", "")
    bounds = element.get("Bounds", [])
    font_info = element.get("Font", {"name": "Helvetica", "size": 12})
    text = element.get("Text", "")

    if bounds and text:
        # Convert bounds to Adobe JSON format
        x1 = bounds[0]
        y1 = pdf_height - bounds[3]  # Flip Y-axis for bottom-left origin
        x2 = bounds[2]
        y2 = pdf_height - bounds[1]

        # Add text element to Adobe JSON
        adobe_element = {
            "type": "text",
            "bounds": [x1, y1, x2, y2],
            "text": text,
            "font": {
                "name": font_info.get("name", "Helvetica"),
                "size": font_info.get("size", 12)
            }
        }
        adobe_json["elements"].append(adobe_element)

# Save Adobe JSON to file
with open(adobe_json_path, "w") as file:
    json.dump(adobe_json, file, indent=4)
print(f"Adobe JSON saved to {adobe_json_path}")
