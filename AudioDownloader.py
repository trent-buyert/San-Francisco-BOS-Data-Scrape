import requests as rq
from bs4 import BeautifulSoup
from datetime import datetime
def download_audio_files(projectPath):
    url = "https://sanfrancisco.granicus.com/ViewPublisher.php?view_id=10"
    content = rq.get(url).content
    soup = BeautifulSoup(content, "html.parser")
    tbody = soup.find("tbody")
    trs = tbody.find_all("tr")
    for tr in trs:
        tds = tr.find_all("td")
        # Trimming undesirable numbers surrounding date
        date = tds[0].text[-8:]
        dateObject = datetime.strptime(date, "%m/%d/%y")
        formattedDate = dateObject.strftime("%b %d, %Y")
        print(formattedDate)
        audioMonth = dateObject.strftime("%B")
        audioYear = dateObject.strftime("%Y")
        # We only want audio files through 2015
        if formattedDate[-4:] == '2014':
            break
        # Extracting meeting name from headers allows me to distinguish the type of meeting for naming purposes
        meetingName = tds[0]['headers'][1]
        fileName = audio_namer(meetingName, formattedDate)
        mp3Anchor = tr.find('a', href=lambda href: href and 'mp3' in href)
        mp3Url = mp3Anchor['href']
        filePath = rf"{projectPath}\{audioYear}\{audioMonth}\{fileName}"
        write_audio_files(date, mp3Url, filePath)


def audio_namer(meetingName, date):
    meetingName = meetingName.lower()
    if 'joint' in meetingName and 'special' in meetingName:
        meetingType = 'Joint Special'
    elif 'joint' in meetingName:
        meetingType = 'Joint'
    elif 'special' in meetingName:
        meetingType = 'Special'
    else:
        meetingType = 'Regular'
    fileName = f"{date}_Meeting {meetingType} Audio.mp3"
    return fileName


def write_audio_files(date, audioFileUrl, fileDownloadPath):
    try:
        audio = rq.get(audioFileUrl)
        with open(fileDownloadPath, "wb") as file:
            print(f"Audio file from {date} downloaded.")
            file.write(audio.content)
    except rq.exceptions.RequestException as e:
        print(f"Failed to download audio file from {date}. Error: {e}")
    except IOError as e:
        print(f"Failed to write audio file from {date} to disk. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
