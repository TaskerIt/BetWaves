from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
from selenium import webdriver

# Define chrome driver
chromedriver = "C:\SeleniumDrivers\chromedriver_win32\chromedriver"
driver = webdriver.Chrome(chromedriver)

#import time
import time
import os

# URl to web scrap from.
# in this example we web scrap graphics cards from Newegg.com
betpage_url = "https://www.betfair.com/exchange/plus/"
#driver.maximize_window
#driver.get(betpage_url)

#time.sleep(5)
#content = driver.page_source.encode('utf-8').strip()
#betpage_soup = soup(content,"html.parser")
#bcontainers = betpage_soup.findAll("tr", {"ng-repeat-start": "(marketId, event) in vm.tableData.events"})
t = 0
driver.get(betpage_url)
time.sleep(5)

while t<100000:
    driver.refresh()
    time.sleep(2)
    content = driver.page_source.encode('utf-8').strip()
    betpage_soup = soup(content,"html.parser")
    bcontainers = betpage_soup.findAll("tr", {"ng-repeat-start": "(marketId, event) in vm.tableData.events"})
    os.system('cls')
    for container in bcontainers:
        # print(container)
        Hometeam = container.find("td",{"class","coupon-runners"}).find("div",{"class":"coupon-runner"}).find("button",{"data-bet-type":"back"})
        print(Hometeam.text.strip())
    t = t+1
    print (t)

driver.close()
