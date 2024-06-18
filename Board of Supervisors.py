import FileStructureCreator
import AgendaDownloader
import AudioDownloader
SFBOSDatascrapePath = rf"C:\Users\Trent\coding\python projects\San Francisco\Board of Supervisors"

FileStructureCreator.file_structure_creator(SFBOSDatascrapePath)
AgendaDownloader.download_agendas(SFBOSDatascrapePath)
AudioDownloader.download_audio_files(SFBOSDatascrapePath)



