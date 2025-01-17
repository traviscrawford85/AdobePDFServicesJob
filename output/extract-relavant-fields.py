import json
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter

# Load the structured JSON
with open("output\ExtractTextInfoFromPDF\extract2025-01-17T10-50-39\structuredData.json", "r") as file:
    structured_json = json.load(file)

# Relevant fields and their JSON paths stored n a variable
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

# Extract bounds and page for each relevant field stored in a variable
extracted_fields = {}
for field, path in relevant_fields.items():
    for element in structured_json["elements"]:
        if element["Path"] == path:
            extracted_fields[field] = {
                "bounds": element["Bounds"],
                "page": element["Page"]
            }
            break

print(extracted_fields)

# Perform Calculations
# Example values from wage transcript stored in a variable
wages = 42688.00
taxable_interest = 11.00
standard_deduction = 6100.00
federal_tax_withheld = 6081.00

# Calculate AGI, taxable income, tax owed, and refund stored in a variable
agi = wages + taxable_interest
taxable_income = agi - standard_deduction
tax_owed = 5075.50  # Pre-calculated for simplicity
refund = federal_tax_withheld - tax_owed

# Values to overlay stored in a variable
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

# Generate Overlay PDF and store it in a variable
output_pdf = "overlay.pdf"
c = canvas.Canvas(output_pdf)

# Draw each field using its extracted bounds
for field, details in extracted_fields.items():
    bounds = details["bounds"]
    value = calculated_values[field]
    x, y = bounds[0], bounds[3]  # Bottom-left corner of the field
    c.drawString(x, y, value)

c.save()
print(f"Overlay PDF saved to {output_pdf}")


# Paths to input and output files
template_pdf = r"resources\forms\2013 Form 1040_Template.pdf"
overlay_pdf = "overlay.pdf"
completed_pdf = "completed_1040.pdf"

reader = PdfReader(template_pdf)
overlay_reader = PdfReader(overlay_pdf)
writer = PdfWriter()

for page_num, page in enumerate(reader.pages):
    if page_num < len(overlay_reader.pages):
        page.merge_page(overlay_reader.pages[page_num])
    writer.add_page(page)

with open(completed_pdf, "wb") as output_file:
    writer.write(output_file)

print(f"Completed PDF saved to {completed_pdf}")
