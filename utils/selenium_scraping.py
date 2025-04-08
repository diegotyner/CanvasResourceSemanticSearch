
import time
import re
import threading

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup


attempts = 3
print_lock = threading.Lock()

def scrape_file_page(driver):
  """
  DO NOT USE THIS METHOD.
  API scraping is much faster

  First, make sure the file page EXISTS, don't run this code until then
  Should be the file page url, of style "https://canvas.ucdavis.edu/courses/961262/files"
  """
  
  element = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.CLASS_NAME, "ef-item-row"))
  )
  print("Files loaded!")

  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  # print(soup.find("body"))

  files = []
  for row in soup.find_all("div", class_="ef-item-row"):
    anchor = row.find("a")
    link = anchor.get("href")
    name = anchor.find("span", class_="ef-name-col__text").text.strip()
    size = row.find("div", class_="ef-size-col").text.strip()

    # not_right_side
    files.append((link, name, size))
  print(files)
  print(len(files))

  driver.quit()
  return files



def scrape_lecture_links(driver, course_url):
  """
  First, make sure the Media Gallery page EXISTS, don't run this code until then
  Should be the file page url, of style "https://canvas.ucdavis.edu/courses/961262/external_tools/5280"
  """
  
  iframe = None
  for i in range(attempts):
    driver.get(course_url + "/external_tools/5280")
    if "UC Davis Canvas Discovery" in driver.title:
      with print_lock:
        print("Auth failed, use valid canvas cookies")
    try:
      iframe = WebDriverWait(driver, 3).until(
          lambda d: d.find_element(By.XPATH, "//*[starts-with(@id, 'tool_content_')]")
      )
      # with print_lock:
      #   print("Iframe found, continuing")
      break
    except:
      # print(f"Iframe not found: {i}")
      time.sleep(2)
  
  if not iframe:
    return set()
  
  iframe_name = iframe.get_attribute("name")

  driver.switch_to.frame(driver.find_element(by=By.NAME, value=iframe_name))
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

  # html = driver.page_source
  # soup = BeautifulSoup(html, "html.parser")
  # print(soup.find("body").prettify())
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

  # element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "channelGallery_scroller_alert")))
  time.sleep(3)

  html = driver.page_source
  soup = BeautifulSoup(html, "html.parser")
  # print(soup.find("body").prettify())


  # the following links are all relative to aggievideo.canvas.ucdavis.edu
  media_links = set()
  for anchor in soup.find_all("a", attrs={"class": "item_link"}):
    link = anchor.get("href")
    media_links.add(link)
  # with print_lock:
  #   # print(media_links)
  #   print(len(media_links))
    # print("If only 15 found, rerun until content loads")

  return media_links


def scrape_transcripts(driver, lecture_url):
  """
  Make sure to use the aggievideo cookies, canvas cookies won't work
  """

  for i in range(attempts):
    driver.get(lecture_url)

    if "Production" == driver.title.strip():
      with print_lock:
        print("Auth failed, use valid cookies")
      break

    try: 
      tab_element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
          (By.XPATH, '//ul[contains(@class, "tabs-container")]//a[@id="tab-attachments-tab"]')
      ))
      tab_element.click()
      time.sleep(0.5)

      html = driver.page_source
      soup = BeautifulSoup(html, "html.parser")
      
      download_pattern = re.compile(r"\.txt$")
      anchor = soup.find("a", title=download_pattern)
      
      if anchor:
        link = anchor.get("href")
        title = soup.find("h1", class_="entryTitle")
        # print(driver.title)
        # print(title.text.strip() if title else "No Title", link)
        return (title.text.strip() if title else "No Title", link)

      else:
        # print(f"[Attempt {i + 1}] Anchor not found, retrying...")
        time.sleep(2)
    except Exception as e:
      # print(f"[Attempt {i + 1}] Error scraping transcripts: {str(e)}")
      time.sleep(2)
  
  return ("Error", "") # This can happen when there is no transcript, like for an empty recording



if __name__ == '__main__':
  print("Running main file")