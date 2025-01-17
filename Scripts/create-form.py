from fpdf import FPDF

# Function to create Form 1040 (Federal Individual Income Tax Return)
def create_form_1040():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Form 1040 - U.S. Individual Income Tax Return (2013)", ln=True, align='C')

    pdf.ln(10)
    pdf.cell(200, 10, txt="Filing Status: Single", ln=True)
    pdf.cell(200, 10, txt="Name: TRAV D CRAW", ln=True)
    pdf.cell(200, 10, txt="SSN: XXX-XX-6680", ln=True)
    pdf.cell(200, 10, txt="Address: 1915 St. Paul Street, Baltimore, MD 21218", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Income Section:", ln=True)
    pdf.cell(200, 10, txt="Wages, Salaries, Tips (Line 7): $42,688.00", ln=True)
    pdf.cell(200, 10, txt="Taxable Interest (Line 8a): $11.00", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Adjusted Gross Income:", ln=True)
    pdf.cell(200, 10, txt="Total Income (Line 22): $42,699.00", ln=True)
    pdf.cell(200, 10, txt="Standard Deduction (Line 40): $6,100.00", ln=True)
    pdf.cell(200, 10, txt="Taxable Income (Line 43): $36,599.00", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Tax and Payments:", ln=True)
    pdf.cell(200, 10, txt="Total Tax Liability: Calculated per IRS tables.", ln=True)
    pdf.cell(200, 10, txt="Federal Tax Withheld (Line 62): $6,081.00", ln=True)
    pdf.cell(200, 10, txt="Refund or Amount Owed: To be finalized.", ln=True)

    return pdf

# Generate Form 1040 PDF
form_1040_pdf = create_form_1040()
form_1040_file_path = "/mnt/data/Form_1040_2013.pdf"
form_1040_pdf.output(form_1040_file_path)

# Provide file to user
form_1040_file_path
