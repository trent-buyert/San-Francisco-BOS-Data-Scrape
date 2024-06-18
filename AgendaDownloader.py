import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
from PdfToHtmlConverter import pdf_to_html_converter
def download_agendas(projectPath):
    #pageModifier exists because we want to scrape the original page before incrementing
    pageModifier = ""
    for counter in range(0, 14):
        if counter > 0:
            pageModifier = f"&page={counter}"
        url = f"https://sfbos.org/events/calendar/past?field_event_category_tid=54{pageModifier}"
        baseUrl = "https://sfbos.org"
        content = rq.get(url).text
        soup = BeautifulSoup(content, "html.parser")
        tbody = soup.find("tbody")
        trs = tbody.find_all("tr")
        for tr in trs:
            tds = tr.find_all("td")
            #dateStringRaw exists because there's a descrepancy in naming conventions.
            dateStringRaw = tds[0].text.strip()
            if "-" in dateStringRaw:
                dateString = dateStringRaw.split("-")
            else:
                dateString = dateStringRaw.split("(")
            dateString = dateString[0].strip()
            dateObject = datetime.strptime(dateString, "%A, %B %d, %Y")
            formattedDate = dateObject.strftime("%b %d, %Y")
            #We are only scraping through 2015
            if formattedDate[-4:] == '2014':
                break
            meetingName = tds[1].find("a").text
            fileName = agenda_namer(meetingName, formattedDate)
            agendaMonth = dateObject.strftime("%B")
            agendaYear = dateObject.strftime("%Y")
            filePath = rf"{projectPath}\{agendaYear}\{agendaMonth}\{fileName}"
            agendaUrl = f"{baseUrl}{tds[1].find('a')['href']}"
            pdf_to_html_converter(formattedDate, agendaUrl, filePath)

def agenda_namer(meetingName, date):
    meetingName = meetingName.lower()
    if 'joint' in meetingName and 'special' in meetingName:
        meetingType = 'Joint Special'
    elif 'joint' in meetingName:
        meetingType = 'Joint'
    elif 'special' in meetingName:
        meetingType = 'Special'
    else:
        meetingType = 'Regular'
    fileName = f"{date}_Meeting {meetingType} Agenda.html"
    return fileName
