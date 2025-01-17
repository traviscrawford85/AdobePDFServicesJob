import json
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

# Paths
structured_json_path = r"output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json"  # Input structured JSON
template_pdf_path = r"resources\forms\2013 Form 1040_Template.pdf"       # Input blank 1040 form
output_overlay_pdf_path = r"output\Completed1040\overlay.pdf"       # Intermediate overlay PDF
output_completed_pdf_path = r"output\Completed1040\completed_1040.pdf"  # Final completed PDF

# Step 1: Define relevant fields and JSON paths
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

# Step 2: Perform calculations
# Example values from wage transcript
wages = 42688.00
taxable_interest = 11.00
standard_deduction = 6100.00
federal_tax_withheld = 6081.00

# Calculate AGI, taxable income, tax owed, and refund
agi = wages + taxable_interest
taxable_income = agi - standard_deduction
tax_owed = 5075.50  # Pre-calculated for simplicity
refund = federal_tax_withheld - tax_owed

# Calculated values
calculated_values = {
    "Line 1 - Wages, salaries, tips": f"{wages:.2f}",
    "Line 2b - Taxable Interest": f"{taxable_interest:.2f}",
    "Line 8b - Adjusted Gross Income": f"{agi:.2f}",
    "Line 9 - Standard Deduction": f"{standard_deduction:.2f}",
    "Line 10 - Taxable Income": f"{taxable_income:.2f}",
    "Line 11 - Tax Owed": f"{tax_owed:.2f}",
    "Line 25d - Federal Income Tax Withheld": f"{federal_tax_withheld:.2f}",
    "Line 34 - Refund": f"{refund:.2f}",
}

# Step 3: Extract bounds from structured JSON
extracted_fields = {}
with open(structured_json_path, "r") as file:
    structured_json = json.load(file)

for field, path in relevant_fields.items():
    for element in structured_json["elements"]:
        if element["Path"] == path:
            extracted_fields[field] = {
                "bounds": element["Bounds"],
                "page": element["Page"]
            }
            break

# Step 4: Generate overlay PDF
overlay_canvas = canvas.Canvas(output_overlay_pdf_path)

for field, details in extracted_fields.items():
    bounds = details["bounds"]
    value = calculated_values[field]
    x, y = bounds[0], bounds[3]  # Bottom-left corner of the field
    overlay_canvas.setFont("Helvetica", 12)
    overlay_canvas.drawString(x, y, value)

overlay_canvas.save()

# Step 5: Combine overlay with template
reader = PdfReader(template_pdf_path)
overlay_reader = PdfReader(output_overlay_pdf_path)
writer = PdfWriter()

for page_num, page in enumerate(reader.pages):
    if page_num < len(overlay_reader.pages):
        page.merge_page(overlay_reader.pages[page_num])
    writer.add_page(page)

with open(output_completed_pdf_path, "wb") as output_file:
    writer.write(output_file)

print(f"Completed PDF saved to {output_completed_pdf_path}")
