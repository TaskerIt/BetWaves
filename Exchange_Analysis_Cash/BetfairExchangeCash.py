from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from selenium import webdriver # Selenium web driver

# Define chrome driver
chromedriver = "C:/SeleniumDrivers/chromedriver_win32/chromedriver"
driver = webdriver.Chrome(chromedriver)

#import time
import time

#import operating system
import os

# Define web scrape URLs

betpage_url = "https://www.betfair.com/exchange/plus/"

# Define variables
t = 0
inittime = time.time()

# Retrieve url content
driver.get(betpage_url)
time.sleep(5) # time delay to permit url opening

while time.time()<inittime+50: # limit run period

    driver.refresh() # refresh content
    time.sleep(2) # time delay to permit content refresh
    content = driver.page_source.encode('utf-8').strip() # strip data
    betpage_soup = soup(content,"html.parser")
    bcontainers = betpage_soup.findAll("tr", {"ng-repeat-start": "(marketId, event) in vm.tableData.events"})
    os.system('cls') # clear print window
    for container in bcontainers:
        oddscontainer = container.findAll("div",{"class":"coupon-runner ng-scope"})
        # Home Team name
        Hometeamn = container.a.find("event-line",{"event-data":"::event"}).section.find("ul",{"class":"runners"}).li
        Hometeam = Hometeamn.text.strip()
        # Away Team name
        Awayteamn = Hometeamn.next_sibling
        Awayteam = Awayteamn.text.strip()

        for ncontainer in oddscontainer:
            
            # Home Team odds
            Hometeamoddsn = ncontainer.find("button",{"data-bet-type":"back"})
            Hometeamodds = Hometeamoddsn.text.strip()
            
            # Away Team odds
            Awayteamoddsn = ncontainer.find("button",{"data-bet-type":"lay"})
            Awayteamodds = Awayteamoddsn.text.strip()
            
            print(Hometeam + ": " + Hometeamodds)
            print(Awayteam + ": " + Awayteamodds)

    t = t+1
    print (t)

driver.close()
