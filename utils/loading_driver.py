from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-dev-shm-usage")

def load_driver(cookies):
  """
  Make sure to pass in a cookie list
  """
  driver = webdriver.Chrome(options=chrome_options)

  for cookie in cookies:
    driver.execute_cdp_cmd('Network.setCookie', cookie)

  return driver


if __name__ == '__main__':
  print("Running main file")