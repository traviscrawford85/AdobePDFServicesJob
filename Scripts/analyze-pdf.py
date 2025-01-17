import json
from PyPDF2 import PdfReader

# Paths
structured_json_path = r"output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json"
template_pdf_path = r"resources\forms\2013 Form 1040_Template.pdf"
output_report_path = r"output\Completed1040\analysis_report.txt"

# Load the structured JSON
with open(structured_json_path, "r") as file:
    structured_json = json.load(file)

# Load the PDF
reader = PdfReader(template_pdf_path)
pdf_width = float(reader.pages[0].mediabox[2])
pdf_height = float(reader.pages[0].mediabox[3])

# Initialize the report content
report_lines = []
report_lines.append(f"PDF Dimensions: {pdf_width} x {pdf_height}\n")
report_lines.append(f"Number of Pages: {len(reader.pages)}\n")
report_lines.append("-" * 50)

# Analyze JSON elements
for element in structured_json["elements"]:
    path = element.get("Path", "")
    bounds = element.get("Bounds", [])
    bbox = element.get("attributes", {}).get("BBox", [0, 0, pdf_width, pdf_height])

    if bounds:
        # Absolute positioning within section BBox
        absolute_x = bbox[0] + bounds[0]
        absolute_y = bbox[1] + bounds[3]
        adjusted_y = pdf_height - absolute_y  # Convert to bottom-left origin

        # Add to report
        report_lines.append(f"Path: {path}")
        report_lines.append(f"  - Bounds: {bounds}")
        report_lines.append(f"  - Section BBox: {bbox}")
        report_lines.append(f"  - Absolute Position: ({absolute_x:.2f}, {adjusted_y:.2f})\n")
        report_lines.append("-" * 50)

# Write the report to a file
with open(output_report_path, "w") as report_file:
    report_file.write("\n".join(report_lines))

print(f"Analysis report saved to: {output_report_path}")
