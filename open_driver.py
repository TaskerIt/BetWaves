from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

class get_driver:
    def __init__(self,url,url_previous):

        # start chrom driver
        if url != "": # check box filled
            try:
                if url == url_previous:
                    # case when matching -> repeat run
                    pass
                else:
                    driver.get(url)
                    time.sleep(2)
                    url_previous = url
                    
            # case when url previous exists
            except:
                self.driver = webdriver.Chrome(executable_path=r"Wave_inputs/Chromedriver.exe")
                self.driver.get(url)
                time.sleep(2)
                url_previous = url
                
                
            # Set language to English
            try:
                self.driver.find_element_by_xpath('//*[@id="ssc-ht"]/tbody/tr/td[6]/div/div[1]/span[2]').click()
                self.driver.find_element_by_xpath('//*[@id="ssc-ht"]/tbody/tr/td[6]/div/div[2]/div/ul/li[1]/a').click()
            except:
                pass

