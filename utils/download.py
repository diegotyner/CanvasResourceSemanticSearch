
import os
import re
import requests

headers = {"User-Agent": "Mozilla/5.0"}


# (name, OG link, download link)
def regex_selector(files):
  input_pattern = input("Regex: ")
  reg_pattern = re.compile(rf"{input_pattern}")

  downloads = []
  for file in files:
    print(f"\tDownload: {file[0]}? ", end="")
    if reg_pattern.search(file[0]):
      downloads.append(file)
      print("y")
    else:
      print("n")
  return downloads

def pdf_pptx_selector(files):
  reg_pattern = re.compile(r"\.(pdf|pptx)$", re.IGNORECASE)

  downloads = []
  for file in files:
    print(f"\tDownload: {file[0]}? ", end="")
    if reg_pattern.search(file[0]):
      downloads.append(file)
      print("y")
    else:
      print("n")
  return downloads

# (name, OG link, download link)
def prompt_selector(files):
  downloads = []
  print("---  Selecting  ---")
  for file in files:
    download = input(f"Download: {file[0]:<40} {file[1] if file[1] else 'Unknown' :>6}? (y/n) ")
    if 'y' in download.lower():
      downloads.append(file)
  return downloads

def file_download(folder_selector, coursename, filename, fileurl, cookies, chunk_size=16384):
  FOLDER_OPTIONS = ['course-downloads', 'course-lectures']
  if folder_selector not in FOLDER_OPTIONS:
    raise ValueError(f"Invalid sim type. Expected one of: {FOLDER_OPTIONS}")
  

  if not fileurl or not fileurl: 
    return False
  

  r = requests.get(fileurl, headers=headers, cookies=cookies, stream=True)
  if r.status_code != 200:
    return False  
  
  os.makedirs(f"{folder_selector}/{coursename}", exist_ok=True)
  filepath_building = f"{folder_selector}/{coursename}/{filename}"

  with open(filepath_building, "wb") as f:
    for chunk in r.iter_content(chunk_size):
      if chunk:
        f.write(chunk)

  return True



if __name__ == '__main__':
  print("Running main file")