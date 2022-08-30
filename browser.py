from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
import random

def userAgent() -> str:
  """Return driver user agent.

  Returns:
      str: Driver user agent
  """
  options = webdriver.ChromeOptions()
  options.add_argument("headless")
  options.add_argument("no-sandbox")
  options.add_argument("remote-debugging-port=9222")
  options.add_argument("disable-gpu")
  d = webdriver.Chrome(options = options)
  res = d.execute_script("return navigator.userAgent;")
  d.close()
  return res.replace("Headless", "").replace("headless", "")

def getDriver() -> WebDriver:
  """Get a web driver.

  Returns:
      WebDriver: Web driver.
  """
  options = webdriver.ChromeOptions()
  options.add_argument("no-sandbox")
  return webdriver.Chrome(options = options)

def getHeadlessDriver(workdir: str) -> WebDriver:
  """Get a (window-less) web driver.

  Args:
      workdir (str): Location for file downloads, etc.

  Returns:
      WebDriver: Web driver.
  """
  options = webdriver.ChromeOptions()
  options.add_argument("headless")
  options.add_argument("no-sandbox")
  options.add_argument(f"port={random.randint(4001,4999)}")
  options.add_argument(f"remote-debugging-port={random.randint(9001,9999)}")
  options.add_argument("disable-gpu")
  options.add_argument("disable-extensions")
  options.add_argument("disable-in-process-stack-traces")
  options.add_argument("disable-logging")
  options.add_argument("disable-dev-shm-usage")
  options.add_argument("log-level=0")
  options.add_argument("silent")
  options.add_argument("output=/dev/null")
  options.add_argument("disable-blink-features=AutomationControlled")
  options.add_argument("window-size=1920,1080")
  options.add_argument(f"user-agent={userAgent()}")  
  options.add_experimental_option("excludeSwitches", ["enable-automation"])
  
  prefs = {
    "download.default_directory": workdir, 
    "prompt_for_download": False
  }
  
  options.add_experimental_option("prefs", prefs)  
  drv = webdriver.Chrome(options = options)  
  drv.implicitly_wait(10)
  return drv
