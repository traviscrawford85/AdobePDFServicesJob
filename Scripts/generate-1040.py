from PyPDF2 import PdfReader, PdfWriter

# Paths to input files
template_pdf_path = r"resources\forms\2013 Form 1040.pdf"  # Path to the original blank 1040 form
overlay_pdf_path = r"output\completed_1040.pdf"  # Generated overlay PDF
final_pdf_path = r"output\final_1040.pdf"        # Output file

# Read the template and overlay PDFs
template_reader = PdfReader(template_pdf_path)
overlay_reader = PdfReader(overlay_pdf_path)
writer = PdfWriter()

# Overlay each page
for page in template_reader.pages:
    overlay_page = overlay_reader.pages[0]
    page.merge_page(overlay_page)
    writer.add_page(page)

# Save the final PDF
with open(final_pdf_path, "wb") as output:
    writer.write(output)

print(f"Final completed 1040 saved to {final_pdf_path}")
