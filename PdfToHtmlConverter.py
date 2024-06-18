import requests
from pdfminer.high_level import extract_text
from io import BytesIO
from html import escape


def pdf_to_html_converter(date, agendaUrl, fileDownloadPath):
    response = requests.get(agendaUrl)
    if response.status_code == 200:
        try:
            pdf_content = BytesIO(response.content)
            pdf_text = extract_text(pdf_content)
            # Convert the text to HTML
            html_content = '<html><body><pre>{}</pre></body></html>'.format(escape(pdf_text))
            # Save the HTML content to a file
            with open(fileDownloadPath, 'w', encoding='utf-8') as file:
                print(f"Downloading agenda from {date}")
                file.write(html_content)
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while downloading the PDF from {date}: {e}")
        except Exception as e:
            print(f"An error occurred during the PDF processing or file writing from {date}: {e}")
    else:
        print(f"Failed to download an agenda from {date}.")