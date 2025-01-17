import json
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

# Paths
structured_json_path = r"output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json"  # Input structured JSON
template_pdf_path = r"resources\forms\2013 Form 1040_Template.pdf"       # Input blank 1040 form
output_overlay_pdf_path = r"output\Completed1040\overlay.pdf"       # Intermediate overlay PDF
output_completed_pdf_path = r"output\Completed1040\completed_1040.pdf"  # Final completed PDF

# Load structured JSON
with open(structured_json_path, "r") as file:
    structured_json = json.load(file)

# Define calculated values
calculated_values = {
    "Line 1 - Wages, salaries, tips": "42688.00",
    "Line 2b - Taxable Interest": "11.00",
    "Line 8b - Adjusted Gross Income": "42699.00",
    "Line 9 - Standard Deduction": "6100.00",
    "Line 10 - Taxable Income": "36599.00",
    "Line 11 - Tax Owed": "5075.50",
    "Line 25d - Federal Income Tax Withheld": "6081.00",
    "Line 34 - Refund": "1005.50",
}

# Extract relevant fields and match sections
relevant_fields = {
    "Line 1 - Wages, salaries, tips": "//Document/Sect/Table/TR[1]/TD",
    "Line 2b - Taxable Interest": "//Document/Sect/Table/TR[2]/TD",
    "Line 8b - Adjusted Gross Income": "//Document/Sect/Table/TR[3]/TD",
    "Line 9 - Standard Deduction": "//Document/Sect/Table/TR[4]/TD",
    "Line 10 - Taxable Income": "//Document/Sect/Table/TR[5]/TD",
    "Line 11 - Tax Owed": "//Document/Sect/Table/TR[6]/TD",
    "Line 25d - Federal Income Tax Withheld": "//Document/Sect/Table/TR[7]/TD",
    "Line 34 - Refund": "//Document/Sect/Table/TR[8]/TD",
}

reader = PdfReader(template_pdf_path)
pdf_width = float(reader.pages[0].mediabox[2])  # 612
pdf_height = float(reader.pages[0].mediabox[3])  # 792

extracted_fields = {}

# Parse JSON to adjust for sections
for field, path in relevant_fields.items():
    for element in structured_json["elements"]:
        if element["Path"] == path:
            element_bounds = element["Bounds"]
            section_bbox = element.get("attributes", {}).get("BBox", [0, 0, pdf_width, pdf_height])

            # Calculate absolute coordinates based on section
            absolute_x1 = section_bbox[0] + element_bounds[0]
            absolute_y1 = section_bbox[1] + element_bounds[1]
            absolute_y2 = section_bbox[1] + element_bounds[3]  # Top of element

            # Convert to bottom-left origin for PDF
            adjusted_x = absolute_x1
            adjusted_y = pdf_height - absolute_y2

            extracted_fields[field] = {"x": adjusted_x, "y": adjusted_y, "text": calculated_values[field]}
            break

# Step 1: Create overlay PDF
overlay_canvas = canvas.Canvas(output_overlay_pdf_path, pagesize=(pdf_width, pdf_height))

for field, details in extracted_fields.items():
    x, y, text = details["x"], details["y"], details["text"]
    overlay_canvas.setFont("Helvetica", 12)
    overlay_canvas.drawString(x, y, text)

overlay_canvas.save()

print(f"Overlay PDF saved to {output_overlay_pdf_path}")

# Step 2: Combine overlay with template
overlay_reader = PdfReader(output_overlay_pdf_path)
writer = PdfWriter()

for page_num, page in enumerate(reader.pages):
    if page_num < len(overlay_reader.pages):
        page.merge_page(overlay_reader.pages[0])
    writer.add_page(page)

with open(output_completed_pdf_path, "wb") as output_file:
    writer.write(output_file)

print(f"Completed 1040 PDF saved to {output_completed_pdf_path}")
