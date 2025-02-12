import logging
import re
import pdfplumber
import pytesseract
from PIL import Image
import tempfile
import os

from .utils import guess_amount, guess_date

class InvoiceExtractor:
    def __init__(self, ocr_engine="tesseract"):
        self.ocr_engine = ocr_engine
        logging.basicConfig(level=logging.INFO)

    def extract_invoice_info(self, subject, sender, attachments):

        invoice_data = {
            "sender": self.parse_sender(sender),
            "invoice_number": None,
            "amount": None,
            "due_date": None,
            "raw_text": ""
        }

        for filename, file_data in attachments:
            # Basic check for PDF file extension
            if filename.lower().endswith(".pdf"):
                text_content = self.extract_text_from_pdf(file_data)
            else:
                # Attempt OCR on images or other file types
                text_content = self.extract_text_with_ocr(file_data)
            invoice_data["raw_text"] += "\n" + text_content

        # Parse out the invoice number, amount, due date
        invoice_data["invoice_number"] = self.find_invoice_number(invoice_data["raw_text"])
        invoice_data["amount"] = guess_amount(invoice_data["raw_text"])
        invoice_data["due_date"] = self.find_due_date(invoice_data["raw_text"])

        return invoice_data

    def parse_sender(self, sender):

        if not sender:
            return ""
        match = re.match(r"(.*?)(<.*>)?", sender)
        if match:
            return match.group(1).strip()
        return sender

    def extract_text_from_pdf(self, pdf_bytes):

        text_content = ""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf_bytes)
            tmp_pdf.flush()
            with pdfplumber.open(tmp_pdf.name) as pdf:
                for page in pdf.pages:
                    # Extract text
                    page_text = page.extract_text()
                    if page_text:
                        text_content += page_text + "\n"

        os.remove(tmp_pdf.name)
        return text_content.strip()

    def extract_text_with_ocr(self, file_data):

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_img:
            tmp_img.write(file_data)
            tmp_img.flush()
            text_content = pytesseract.image_to_string(Image.open(tmp_img.name))

        os.remove(tmp_img.name)
        return text_content.strip()

    def find_invoice_number(self, text):

        patterns = [
            r"(?i)invoice\s*#?\s*(\d+)",           # e.g. "invoice # 12345"
            r"(?i)rechnung\s*#?\s*(\d+)",          # e.g. "rechnung 12345"
            r"(?i)inv\s*#?\s*(\d+)",               # e.g. "inv 12345"
            r"(?i)invoice\s*number:\s*(\d+)",      # e.g. "Invoice Number: 12345"
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        return None

    def find_due_date(self, text):

        match = re.search(r"(?i)due\s*date:\s*(\d{4}-\d{2}-\d{2})", text)
        if match:
            return match.group(1)

        return guess_date(text)
