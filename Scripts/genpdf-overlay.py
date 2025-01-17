from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

# Load the JSON
import json
with open("output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json", "r") as file:
    data = json.load(file)

# Map of new data to be overlaid
new_data = {
    "//Document/Sect/Table/TR/TD/P[4]": "Updated Income Tax Return",
    "//Document/Sect/Table/TR/TD[2]/P": "2025",
}

# Create a new PDF with overlays
overlay_pdf = "overlay.pdf"
c = canvas.Canvas(overlay_pdf)

# Loop through elements in JSON and overlay new data
for element in data["elements"]:
    path = element.get("Path")
    bounds = element.get("Bounds")
    text = new_data.get(path)

    if text and bounds:
        x1, y1, x2, y2 = bounds
        x = x1
        y = y2  # Align at the top of the bounds
        c.setFont("Helvetica", element.get("TextSize", 12))
        c.drawString(x, y, text)

c.save()

# Combine with the original template
template_pdf = "template.pdf"  # Path to your letterhead/template PDF
output_pdf = "output_with_overlays.pdf"

reader = PdfReader(template_pdf)
writer = PdfWriter()

# Add overlay to each page of the template
with open(overlay_pdf, "rb") as overlay:
    overlay_reader = PdfReader(overlay)
    for page in reader.pages:
        page.merge_page(overlay_reader.pages[0])  # Overlay the first page
        writer.add_page(page)

with open(output_pdf, "wb") as output:
    writer.write(output)

print("Overlay complete! Check:", output_pdf)
