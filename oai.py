# -*- coding: utf-8 -*-
"""


@author: patry
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
  
    os.makedirs(PDF_DIR, exist_ok=True)


    sickle = Sickle(OAI_ENDPOINT)


    records = sickle.ListRecords(metadataPrefix='oai_dc')

    with open(CSV_FILENAME, mode="w", encoding="utf-8", newline="") as csv_file:

        fieldnames = [
            "record_id",
            "title",
            "creator",
            "subject",
            "description",
            "publisher",
            "date",
            "type",
            "format",
            "identifier",
            "source",
            "language",
            "relation",
            "coverage",
            "rights"
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
                print(f"Pobrano {i} rekordów...")

    print("Zakończono pobieranie metadanych i zapisywanie do CSV.")

def download_pdf(url):
    """Pobiera plik PDF z podanego adresu URL i zapisuje go w katalogu PDF_DIR."""
    try:

        filename = url.split("/")[-1]
        filepath = os.path.join(PDF_DIR, filename)

  
        if os.path.exists(filepath):
            return

        response = requests.get(url, timeout=20)
        response.raise_for_status()

        with open(filepath, "wb") as f:
            f.write(response.content)
        print(f"Zapisano PDF: {filepath}")

    except Exception as e:
        print(f"Nie udało się pobrać PDF z {url}. Błąd: {e}")

if __name__ == "__main__":
    main()
    
    
    

