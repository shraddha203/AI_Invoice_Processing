import logging
from configparser import ConfigParser

from invoiceProcessor.emailFetcher import EmailFetcher
from invoiceProcessor.invoiceExtractor import InvoiceExtractor
from invoiceProcessor.storage import Storage

def main():
    logging.basicConfig(level=logging.INFO)

    # Read config
    config = ConfigParser()
    config.read("config.ini")

    # 1. Fetch emails
    email_fetcher = EmailFetcher(config_path="config.ini")
    emails = email_fetcher.fetch_invoices()

    # 2. Extract invoice data
    ocr_engine = config["GENERAL"].get("OCR_ENGINE", "tesseract")
    extractor = InvoiceExtractor(ocr_engine=ocr_engine)

    # 3. Store in JSON
    storage = Storage()

    for email_meta in emails:
        # If there's at least one attachment
        if len(email_meta["attachments"]) > 0:
            invoice_data = extractor.extract_invoice_info(
                subject=email_meta["subject"],
                sender=email_meta["sender"],
                attachments=email_meta["attachments"]
            )

            logging.info(f"Storing invoice from '{invoice_data['sender']}' with invoice number '{invoice_data['invoice_number']}'.")
            storage.store_invoice_data(invoice_data)
        else:
            logging.info(f"No attachments found for email: {email_meta['subject']}")

    # 4. Disconnect
    email_fetcher.disconnect()

if __name__ == "__main__":
    main()
