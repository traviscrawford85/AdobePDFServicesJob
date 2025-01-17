from reportlab.pdfgen import canvas

# 1040 data to overlay
calculated_data = {
    "Wages, salaries, tips": {"value": "42,688.00", "position": (100, 750)},  # Line 1
    "Taxable Interest": {"value": "11.00", "position": (100, 720)},          # Line 2b
    "Adjusted Gross Income": {"value": "42,699.00", "position": (100, 690)}, # Line 8b
    "Standard Deduction": {"value": "6,100.00", "position": (100, 660)},     # Line 9
    "Taxable Income": {"value": "36,599.00", "position": (100, 630)},        # Line 10
    "Tax Owed": {"value": "5,075.50", "position": (100, 600)},               # Line 11
    "Federal Income Tax Withheld": {"value": "6,081.00", "position": (100, 570)}, # Line 25d
    "Refund": {"value": "1,005.50", "position": (100, 540)},                 # Line 34
}

# Create a new PDF
output_pdf_path = r"output\completed_1040.pdf"
c = canvas.Canvas(output_pdf_path)

# Add a title or header if needed
c.setFont("Helvetica-Bold", 8)
c.drawString(200, 800, "Form 1040 (2013)")
c.setFont("Helvetica", 8)

# Overlay the calculated data
for label, info in calculated_data.items():
    value = info["value"]
    x, y = info["position"]
    c.drawString(x, y, f"{label}: {value}")

# Save the PDF
c.save()

print(f"Completed PDF saved to {output_pdf_path}")
