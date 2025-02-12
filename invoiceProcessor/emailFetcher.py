import os
import imaplib
import email
from email.header import decode_header
import re
import logging
from configparser import ConfigParser


class EmailFetcher:
    def __init__(self, config_path="config.ini"):
        self.config = ConfigParser()
        self.config.read(config_path)

        self.host = self.config["EMAIL"]["HOST"]
        self.port = self.config["EMAIL"]["PORT"]
        self.username = self.config["EMAIL"]["USERNAME"]
        self.password = self.config["EMAIL"]["PASSWORD"]
        self.folder = self.config["EMAIL"].get("FOLDER", "INBOX")

        self.connection = None
        logging.basicConfig(level=logging.INFO)

    def connect(self):
        self.connection = imaplib.IMAP4_SSL(self.host, self.port)
        self.connection.login(self.username, self.password)
        logging.info("Connected to the IMAP server.")

    def fetch_invoices(self):

        if not self.connection:
            self.connect()

        self.connection.select(self.folder)

        status, message_ids = self.connection.search(None, '(OR SUBJECT "invoice" SUBJECT "rechnung")')

        if status != "OK":
            logging.error("No messages found!")
            return []

        message_list = []
        for num in message_ids[0].split():
            status, data = self.connection.fetch(num, "(RFC822)")
            if status != "OK":
                logging.error(f"Failed to fetch email with ID {num}")
                continue

            msg = email.message_from_bytes(data[0][1])

            # Decode subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8", errors="ignore")

            # Extract sender
            sender = msg.get("From")

            # Check attachments
            attachments = []
            if msg.is_multipart():
                for part in msg.walk():
                    content_disposition = str(part.get("Content-Disposition", ""))
                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            attachments.append((filename, part.get_payload(decode=True)))

            message_list.append({
                "email_id": num.decode(),
                "subject": subject,
                "sender": sender,
                "attachments": attachments
            })

        return message_list

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection.logout()
