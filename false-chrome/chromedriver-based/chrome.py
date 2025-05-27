from selenium import webdriver
import chromedriver_autoinstaller
from time import sleep

chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
                                      # and if it doesn't exist, download it automatically,
                                      # then add chromedriver to path

driver = webdriver.Chrome()

while True:
    sleep(1)
    package = {"url": driver.current_url, "cookies": driver.get_cookies()}
    print(package)
    