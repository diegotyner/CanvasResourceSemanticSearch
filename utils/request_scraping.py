
import requests
import re
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

def get_course_tuples(cookies):
  """
  cookies = A cookie dict, as loaded by create cookie dict util

  Returns: list of tuples: (course_url, class_name)
  """

  course_tuples = []

  url = "https://canvas.ucdavis.edu/courses" # Its a static URL, always this page to see all courses
  r = requests.get(url, cookies=cookies)
  soup = BeautifulSoup(r.text, "html.parser")
  if (soup.find("title").text.strip() == "UC Davis Canvas Discovery"):
    print("Auth failed, use valid canvas cookies")

  for tbody in soup.find_all("tbody"):
    # Find all <tr> rows inside this <tbody>
    for row in tbody.find_all("tr"):
      link = row.find("a")  # Finds the first <a> inside the row
      if link:
        # print(f"Text: {link.text.strip()} - URL: {link.get('href')}")
        course_tuples.append((link.get("href"), link.text.strip()))
  return course_tuples

def get_course_sections(url, cookies):
  """
  url = course homepage, of style https://canvas.ucdavis.edu/courses/822208
  cookies = Cookie dict 

  Returns: list of tuples: (homepage, sect_names) 
    - homepage = "Home" | Section Name like "Modules" | "?" if it breaks
    - sect_names is a dict of all the sections a course uses
  """

  # baseurl = "https://canvas.ucdavis.edu"

  r = requests.get(url, headers=headers, cookies=cookies)
  soup = BeautifulSoup(r.text, "html.parser")
  if (soup.find("title").text.strip() == "UC Davis Canvas Discovery"):
    print("Auth failed, use valid canvas cookies")
  # print(soup.prettify())

  sections_tabs = soup.find(id="section-tabs")
  sections = sections_tabs.find_all("a")
  sect_names = set()
  for section in sections:
    sect_names.add(section.text.strip())
  # print(sect_names)
  # print(f"F: {'Files' in sect_names} | M: {'Modules' in sect_names} | MG: {'Media Gallery' in sect_names}")


  # finding page location:
  element = soup.find(id="breadcrumbs")
  crumbs = element.find_all(class_="ellipsible")
  
  homepage = ""
  
  # crumb 1 is screnreader
  # crumb 2 is classname
  # class 3 is optional homepage redirect
  if len(crumbs) == 2:
    # print("Using normal homepage")
    homepage = "Home"
  elif len(crumbs) == 3:
    # print(crumbs[2].text.strip())
    homepage = crumbs[2].text.strip()
  else:
    # print("not 2 or 3? huuhh?? - ", len(crumbs))
    homepage = "?"

  return (homepage, sect_names)

def scrape_modules_page(url, cookies):
  """
  url = course homepage, of style https://canvas.ucdavis.edu/courses/822208
  cookies = Cookie dict 

  Returns: list of tuples of form: (name, link)
  """

  r = requests.get(url, headers=headers, cookies=cookies)
  soup = BeautifulSoup(r.text, "html.parser")
  if (soup.find("title").text.strip() == "UC Davis Canvas Discovery"):
    print("Auth failed, use valid canvas cookies")

  module_box = soup.find(id="context_modules")

  resources = []
  for row in module_box.find_all("span", class_="item_name"):
    anchor = row.find("a")
    if not anchor:
      continue
    link = anchor.get("href")
    name = anchor.text.strip()
    partition = name.split(".")
    if partition[-1] in ["pdf", "txt", "pptx", "mp4", "csv", "ipynb", "py", "c", "cpp"]:
      resources.append((name, link))
    # else:
    #   print(name)
  return resources

def scrape_module_entry(url, cookies):
  """
  url = file module url, of style https://canvas.ucdavis.edu/courses/948282/modules/items/2177342
  cookies = Cookie dict 

  Returns: list of tuples of form: (file_size, download_link)
  """
  r = requests.get(url, headers=headers, cookies=cookies)
  soup = BeautifulSoup(r.text, "html.parser")
  if (soup.find("title").text.strip() == "UC Davis Canvas Discovery"):
    print("Auth failed, use valid canvas cookies")
  # print(soup.prettify()
  
  try:
    download_anchor = soup.find('a', {'download': 'true'})
    download_link = download_anchor.get("href")

    # Find the file size, which is within a div with no unique parent and no attributes 
    divs = soup.find(id="content").find_all("div")
    file_size = ""
    for i, div in enumerate(divs):
      div_text = div.text.strip()
      file_size_match = re.search(r'\(([^)]+)\)$', div_text)
      if file_size_match:
        # print(file_size_match.group(1))
        file_size = file_size_match.group(1)
    if file_size == "":
      print("no file size found?")
    # print("File Size:", file_size)
    # print("Download Link:", download_link)
    return (file_size, download_link)
  except:
    # print(soup.prettify())
    print(f"Error processing: {soup.find('title').text.strip()}")
    return (None, None)



if __name__ == '__main__':
  print("Running main file")