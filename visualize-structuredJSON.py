from reportlab.pdfgen import canvas
import json

# Paths
structured_json_path = r"output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json"
debug_pdf_path = r"output\Completed1040\debug_visualization.pdf"

# Load structured JSON
with open(structured_json_path, "r") as file:
    structured_json = json.load(file)

# PDF dimensions
pdf_width, pdf_height = 612, 792  # Letter size

# Create a debug PDF
debug_canvas = canvas.Canvas(debug_pdf_path, pagesize=(pdf_width, pdf_height))

# Draw elements
for element in structured_json["elements"]:
    path = element.get("Path", "")
    bounds = element.get("Bounds", [])
    bbox = element.get("attributes", {}).get("BBox", [0, 0, pdf_width, pdf_height])

    if bounds:
        # Calculate absolute positions
        absolute_x1 = bbox[0] + bounds[0]
        absolute_y1 = bbox[1] + bounds[1]
        absolute_x2 = bbox[0] + bounds[2]
        absolute_y2 = bbox[1] + bounds[3]

        # Adjust for PDF's bottom-left origin
        adjusted_y1 = pdf_height - absolute_y2
        adjusted_y2 = pdf_height - absolute_y1

        # Draw bounding box
        debug_canvas.setStrokeColorRGB(1, 0, 0)  # Red for bounds
        debug_canvas.rect(absolute_x1, adjusted_y1, absolute_x2 - absolute_x1, adjusted_y2 - adjusted_y1, stroke=1)

        # Label the field
        debug_canvas.setFont("Helvetica", 6)
        debug_canvas.drawString(absolute_x1, adjusted_y2 + 2, path)

# Save the debug visualization
debug_canvas.save()
print(f"Debug visualization saved to: {debug_pdf_path}")
