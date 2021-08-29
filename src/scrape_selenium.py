from selenium import webdriver
# Using Internet Explorer
# browser = webdriver.Ie()
# Using Edge Chromium
# needs "msedgedriver.exe" otherwize expects "MicrosoftWebDriver.exe"
browser = webdriver.Edge(executable_path="C:/Users/sWege/projects/datakicker/env/msedgedriver.exe")
browser.get('http://seleniumhq.org/')


