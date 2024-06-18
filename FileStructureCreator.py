import os

years = ['2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
months = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
def file_structure_creator(projectPath):
    for year in years:
        for month in months:
            if not os.path.exists(rf"{projectPath}\{year}\{month}"):
                os.makedirs(rf"{projectPath}\{year}\{month}")
