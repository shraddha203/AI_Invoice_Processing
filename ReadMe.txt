1.The solution includes:

Email processing using Python’s imaplib or IMAP client libraries.
Data extraction from PDFs using pdfplumber or PyPDF2, plus pytesseract for OCR if the PDF is image-based.
Presentation of the final data in JSON.

2. Features
a.Email Analysis

Connects to an IMAP mailbox.
Searches for emails with “invoice” or “rechnung” in the subject (configurable).
Extracts attachments (PDFs, images) for processing.

b.Invoice Data Extraction

Identifies Sender (from either email headers or PDF text).
Locates Invoice Number, Amount, and Due Date using regex and/or OCR.
Leverages OCR (pytesseract) if the PDF text can’t be directly extracted.

c.Data Storage

Fallback to JSON output.

d.Presentation

Outputs structured JSON.

----------------------------------------------------------------------------------
config.ini: Holds IMAP and DB credentials, plus general settings (OCR engine, etc.).
requirements.txt: Python dependencies.
main.py: Main script to orchestrate fetching, extraction, and storing.
invoiceProcessor/:
emailFetcher.py: Handles IMAP connection and message retrieval.
invoiceExtractor.py: Extracts text from PDFs/attachments and parses out invoice details.
storage.py: Saves the extracted data (DB or JSON).
utils.py: Helper functions (regex for amounts/dates, OCR utilities, etc.).

----------------------------------------------------------------------------------
Setup & Installation

1. Create a Virtual Environment
venv\Scripts\activate          # Windows

2.Install Dependencies
pip install -r requirements.txt

3.Install OCR Tool
https://tesseract-ocr.github.io/tessdoc/Downloads.html

4.Configure config.ini
Under [EMAIL], specify your IMAP host/port, username, and password.
Under [DATABASE], set TYPE to postgres, mongo, or none

5.Run main script
python main.py

