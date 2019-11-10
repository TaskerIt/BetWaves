from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

class get_driver:
    def __init__(self,url):
        from Wave_inputs import globals
        # start chrome driver
        if url != "": # check box filled
            try:
                if url == globals.url:
                    # case when matching -> repeat run
                    self.driver = globals.global_driver
                else:
                    # case when not matching -> new run
                    self.driver = globals.global_driver
                    self.driver.get(url)
                    time.sleep(2)
                    # store globals URL
                    globals.url = url
            except:
                # case where new driver is required -> first run
                self.driver = webdriver.Chrome(executable_path=r"Wave_inputs/Chromedriver.exe")
                self.driver.get(url)
                # sleep to allow driver to open
                time.sleep(2)
                # store globals driver
                globals.global_driver = self.driver
                # store globals URL
                globals.url = url

            # =============== Generic Actions to local driver ===================
            #  Maximise window
            try:
                self.driver.maximize_window()
            except:
                pass
            # Set language to English
            try:
                self.driver.find_element_by_xpath('//*[@id="ssc-ht"]/tbody/tr/td[6]/div/div[1]/span[2]').click()
                self.driver.find_element_by_xpath('//*[@id="ssc-ht"]/tbody/tr/td[6]/div/div[2]/div/ul/li[1]/a').click()
            except:
                pass

