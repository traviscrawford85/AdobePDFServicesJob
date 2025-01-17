"""
 Copyright 2024 Adobe
 All Rights Reserved.

 NOTICE: Adobe permits you to use, modify, and distribute this file in
 accordance with the terms of the Adobe license agreement accompanying it.
"""

import logging
import os
from datetime import datetime
from dotenv import load_dotenv  # Import dotenv

from adobe.pdfservices.operation.auth.service_principal_credentials import ServicePrincipalCredentials
from adobe.pdfservices.operation.exception.exceptions import ServiceApiException, ServiceUsageException, SdkException
from adobe.pdfservices.operation.io.cloud_asset import CloudAsset
from adobe.pdfservices.operation.io.stream_asset import StreamAsset
from adobe.pdfservices.operation.pdf_services import PDFServices
from adobe.pdfservices.operation.pdf_services_media_type import PDFServicesMediaType
from adobe.pdfservices.operation.pdfjobs.jobs.extract_pdf_job import ExtractPDFJob
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_element_type import ExtractElementType
from adobe.pdfservices.operation.pdfjobs.params.extract_pdf.extract_pdf_params import ExtractPDFParams
from adobe.pdfservices.operation.pdfjobs.result.extract_pdf_result import ExtractPDFResult

# Load environment variables from .env
load_dotenv()

# Initialize the logger
logging.basicConfig(level=logging.INFO)

class ExtractTextInfoFromPDF:
    def __init__(self):
        try:
            # Open the file
            with open(r"resources\201312_Wage and Income_CRAW_105175422850.pdf", "rb") as file:
                input_stream = file.read()

            # Fetch credentials from environment variables
            client_id = os.getenv('PDF_SERVICES_CLIENT_ID')
            client_secret = os.getenv('PDF_SERVICES_CLIENT_SECRET')

            # Validate the credentials
            if not client_id or not client_secret:
                raise ValueError("Missing environment variables: PDF_SERVICES_CLIENT_ID or PDF_SERVICES_CLIENT_SECRET")

            # Initialize credentials
            credentials = ServicePrincipalCredentials(
                client_id=client_id,
                client_secret=client_secret
            )

            # Create a PDF Services instance
            pdf_services = PDFServices(credentials=credentials)

            # Upload the input file
            input_asset = pdf_services.upload(input_stream=input_stream, mime_type=PDFServicesMediaType.PDF)

            # Define the parameters for the job
            extract_pdf_params = ExtractPDFParams(
                elements_to_extract=[ExtractElementType.TEXT],
            )

            # Create and submit the job
            extract_pdf_job = ExtractPDFJob(input_asset=input_asset, extract_pdf_params=extract_pdf_params)
            location = pdf_services.submit(extract_pdf_job)

            # Get the job result
            pdf_services_response = pdf_services.get_job_result(location, ExtractPDFResult)

            # Get the resulting asset
            result_asset: CloudAsset = pdf_services_response.get_result().get_resource()
            stream_asset: StreamAsset = pdf_services.get_content(result_asset)

            # Write the result to an output file
            output_file_path = self.create_output_file_path()
            with open(output_file_path, "wb") as file:
                file.write(stream_asset.get_input_stream())
                logging.info(f"Text extraction completed. Output saved to: {output_file_path}")

        except ServiceApiException as service_api_exception:
            self.handle_exception("ServiceApiException", service_api_exception.message, service_api_exception.status_code)
        except ServiceUsageException as service_usage_exception:
            self.handle_exception("ServiceUsageException", service_usage_exception.message, service_usage_exception.status_code)
        except SdkException as sdk_exception:
            self.handle_exception("SdkException", sdk_exception.message, None)

    @staticmethod
    def create_output_file_path() -> str:
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        os.makedirs("output/ExtractTextInfoFromPDF", exist_ok=True)
        return f"output/ExtractTextInfoFromPDF/extract{time_stamp}.zip"

    @staticmethod
    def handle_exception(exception_type, exception_message, status_code) -> None:
        logging.error(f"{exception_type}: {exception_message} (Status Code: {status_code})")

if __name__ == "__main__":
    ExtractTextInfoFromPDF()
