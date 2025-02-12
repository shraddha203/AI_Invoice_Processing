import logging
import json

class Storage:
    def __init__(self):

        logging.basicConfig(level=logging.INFO)
        logging.info("Storage initialized: JSON only (no DB).")

    def store_invoice_data(self, invoice_data):

        logging.info("Storing invoice data in invoices.json (local file).")
        with open("invoices.json", "a", encoding="utf-8") as f:
            json.dump(invoice_data, f, ensure_ascii=False)
            f.write("\n")
