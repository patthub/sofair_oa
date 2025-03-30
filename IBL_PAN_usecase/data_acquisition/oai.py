# -*- coding: utf-8 -*-
"""
Script to fetch metadata records from the OAI endpoint of the Iberica journal,
store them in a CSV file, and download associated PDF files.

Author: patry
"""

from sickle import Sickle
from sickle.models import Record
import requests
import csv
import os

OAI_ENDPOINT = "https://revistaiberica.org/index.php/iberica/oai"
CSV_FILENAME = "metadane_iberica.csv"
PDF_DIR = "pdfy"

def main():
    """
    Main function that fetches metadata records from the OAI endpoint, saves the metadata
    in a CSV file, and downloads PDFs associated with the records.
    """
    os.makedirs(PDF_DIR, exist_ok=True)
    sickle = Sickle(OAI_ENDPOINT)
    records = sickle.ListRecords(metadataPrefix='oai_dc')
    with open(CSV_FILENAME, mode="w", encoding="utf-8", newline="") as csv_file:
        fieldnames = [
            "record_id", "title", "creator", "subject", "description", "publisher",
            "date", "type", "format", "identifier", "source", "language", "relation", 
            "coverage", "rights"
        ]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for i, record in enumerate(records, start=1):
            if record.deleted:
                continue
            md = record.metadata
            row = {
                "record_id": record.header.identifier,
                "title": ", ".join(md.get("title", [])),
                "creator": ", ".join(md.get("creator", [])),
                "subject": ", ".join(md.get("subject", [])),
                "description": ", ".join(md.get("description", [])),
                "publisher": ", ".join(md.get("publisher", [])),
                "date": ", ".join(md.get("date", [])),
                "type": ", ".join(md.get("type", [])),
                "format": ", ".join(md.get("format", [])),
                "identifier": ", ".join(md.get("identifier", [])),
                "source": ", ".join(md.get("source", [])),
                "language": ", ".join(md.get("language", [])),
                "relation": ", ".join(md.get("relation", [])),
                "coverage": ", ".join(md.get("coverage", [])),
                "rights": ", ".join(md.get("rights", [])),
            }
            writer.writerow(row)
            possible_links = md.get("identifier", []) + md.get("relation", [])
            for link in possible_links:
                if link.lower().endswith(".pdf"):
                    download_pdf(link)
            if i % 50 == 0:
                print(f"Downloaded {i} records...")
    print("Finished downloading metadata and saving to CSV.")

def download_pdf(url):
    """
    Downloads a PDF file from the given URL and saves it in the PDF_DIR directory.
    Args:
        url (str): The URL of the PDF to download.
    """
    try:
        filename = url.split("/")[-1]
        filepath = os.path.join(PDF_DIR, filename)
        if os.path.exists(filepath):
            return
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Saved PDF: {filepath}")
    except Exception as e:
        print(f"Failed to download PDF from {url}. Error: {e}")

if __name__ == "__main__":
    main()
