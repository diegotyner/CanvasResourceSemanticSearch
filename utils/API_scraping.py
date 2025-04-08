
import requests
import urllib.parse

headers = {"User-Agent": "Mozilla/5.0"}

# https://stackoverflow.com/questions/1094841/get-a-human-readable-version-of-a-file-size
def sizeof_fmt(num, suffix="B"):
  for unit in ("", "K", "M", "G", "T", "P", "E", "Z"):
    if abs(num) < 1024.0:
      return f"{num:3.1f}{unit}{suffix}"
    num /= 1024.0
  return f"{num:.1f}Y{suffix}"

def get_course_files(course_id, cookies):
  url = f"https://canvas.ucdavis.edu/api/v1/courses/{course_id}/files?%3Fsearch_term=&per_page=10000"
  r = requests.get(url, cookies=cookies)

  if r.status_code != 200:
    print(f"Error fetching files: {r.status_code}")
    return []  # Return empty to avoid further errors
  file_data = r.json()

  # Want these files to be of form: (name, size, URL)
  files = []

  try: 
    for file in file_data:
      name = file["display_name"]
      if isinstance(file["size"], (int, float)): 
          size = sizeof_fmt(file["size"])
      else:
        size = file["size"]
      url = file["url"]
      files.append((name, size, url))

    return files
  except:
    print(file_data)
    return []



def scrape_course_files(course_id, cookies):
  url = f"https://canvas.ucdavis.edu/api/v1/courses/{course_id}/folders/root"
  r = requests.get(url, cookies=cookies)

  if r.status_code != 200:
    print(f"Error fetching files: {r.status_code}")
    return []  # Return empty to avoid further errors
  root_data = r.json()

  # Want these files to be of form: (name, size, URL)
  files = []
  
  if root_data["folders_count"] != 0:
    r = requests.get(root_data['folders_url'], cookies=cookies)
    root_folder_data = r.json()
    folder_dict = {}
    for folder_data in root_folder_data:
      if folder_data["files_count"] == 0 and folder_data["folders_count"] == 0: # 0 files not good enough, could have deeply nested files
        continue
      folder_dict[folder_data["name"]] = recursive_file_extract(folder_data["id"], cookies, folder_data["files_count"], folder_data["folders_count"])
    files.append(folder_dict)

  if root_data["files_count"] != 0:
    r = requests.get(root_data['files_url'], cookies=cookies)
    root_file_data = r.json()
    for file_data in root_file_data:
      name = file_data["display_name"]
      size = sizeof_fmt(file_data["size"])
      url = file_data["url"]
      files.append((name, size, url))
  
  return files


    

def recursive_file_extract(folder_id, cookies, files_count, folders_count):
  # https://canvas.ucdavis.edu/api/v1/courses/{course_id}/folders/by_path/Homework%20and%20Journal%20Assignments
  # https://canvas.ucdavis.edu/api/v1/folders/3933004/folders
  # https://canvas.ucdavis.edu/api/v1/folders/3933004/files

  files = []
  if files_count > 0:
    files_url = f"https://canvas.ucdavis.edu/api/v1/folders/{folder_id}/files"
    file_r = requests.get(files_url, cookies=cookies)

    if file_r.status_code != 200:
      print(f"Error fetching files: {file_r.status_code}")
      return files  # Return empty to avoid further errors

    file_data = file_r.json()

    for file in file_data:
      name = file["display_name"]
      size = sizeof_fmt(file["size"])
      url = file["url"]
      files.append((name, size, url))

  if folders_count > 0:
    folder_url = f"https://canvas.ucdavis.edu/api/v1/folders/{folder_id}/folders"
    folder_r = requests.get(folder_url, cookies=cookies)
    if folder.status_code != 200:
      print(f"Error fetching files: {folder.status_code}")
      return files  # Return empty to avoid further errors

    folder_data = folder_r.json()

    folder_dict = {}
    for folder in folder_data:
      if folder["files_count"] == 0 and folder["folders_count"] == 0: # 0 files not good enough, could have deeply nested files
        continue
      folder_dict[folder["name"]] = recursive_file_extract(folder["id"], cookies, folder["files_count"], folder["folders_count"])
    files.append(folder_dict)
  return files

if __name__ == '__main__':
  print("Running main file")