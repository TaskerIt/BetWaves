
import time

class execute_trade_back_lay:
    def __init__(self,driver,league,sub_table,row,market,back_cash,back_odds,lay_odds):
        
        # confirm odds expected:
        

        if market == "home":
            market_col = 1
            market_col_sub_back = 1
            market_col_sub_lay = 2 
        elif market == "draw":
            market_col = 2
            market_col_sub_back = 1
            market_col_sub_lay = 2
        elif market == "away":
            market_col = 3
            market_col_sub_back = 1
            market_col_sub_lay = 2     
        else:
            pass
        
        

        # !!!!!!!!!!!!! IMPORTANT - When clicking the button, the insert field represents an added row so this insert field row must be an offset +1
        enter_row = row+1

        try:
            # Click back a trade
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[{market_col}]/button[{market_col_sub_back}]').click()
            
            # Define bet stake
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div/div[2]/div[2]/div/input').send_keys(back_cash)

            # place bet
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div/div[2]/button[3]').click()

            time.sleep(0.5)

            # Confirm bet
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div/div[2]/button[3]').click()

            # wait for bet to be approved
            time.sleep(7)
            
            
            # Click lay a trade
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[{market_col}]/button[{market_col_sub_lay}]').click()
            
            time.sleep(1)

            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div[2]/div[2]/div[1]/div/input').clear()

            # Define lay odds
                                          #//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section/div[2]/bf-coupon-table[1]/div/table/tbody/tr[4]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div[2]/div[2]/div[1]/div/input
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div[2]/div[2]/div[1]/div/input').send_keys(str(lay_odds))  
            #driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div/div[2]/div[1]/div/input').send_keys(lay_odds)     
            
            # Define bet stake
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div[2]/div[2]/div[2]/div/input').send_keys(back_cash)

            # place bet
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div[2]/div[2]/button[3]').click()

            time.sleep(0.5)

            # Confirm bet
            driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div[2]/div[2]/button[3]').click()

            # wait for bet to be approved
            time.sleep(7)




            # last step
            self.result = True

            driver.refresh()
            #time.sleep(2)
        except:
            driver.refresh()
            #time.sleep(2)
            self.result = False
    
    
        
