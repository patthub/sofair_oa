# -*- coding: utf-8 -*-
"""


@author: patry
"""
import pandas as pd
import os
import requests

df = pd.read_csv("metadane_iberica.csv")
links = list(df["relation"])


def download_pdfs(links, download_folder):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for url in links:

        filename = url.split("/")[-1] + ".pdf"
        file_path = os.path.join(download_folder, filename)

        try:

            url = url.replace("view", "download")
            response = requests.get(url)
            response.raise_for_status()  

            with open(file_path, 'wb') as f:
                f.write(response.content)
            print(f"Plik {filename} został pobrany.")

        except requests.exceptions.RequestException as e:
            print(f"Nie udało się pobrać pliku z {url}. Błąd: {e}")


download_folder = "pobrane_pdfy_iberica"
download_pdfs(links, download_folder)