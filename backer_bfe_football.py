
import time

def back_draw_trade(row,league,sub_table,c):
    try:
        if sub_table == 0:
            sub_table = ""
        else:
            sub_table = f'[{sub_table}]'
    except:
        pass

    # !!!!!!!!!!!!! IMPORTANT - When clicking the button, the insert field represents an added row so this insert field row must be an offset +1
    enter_row = row+1

    try:
        # Click back a draw trade
        driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[2]/button[1]').click()

        # Define back odds
        driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{enter_row}]/td/ng-include/inline-betting-wrapper/bf-inline-betting/section/div/div/div/div[2]/div[1]/div/input').send_keys(back_cash)     
        
        # Click to close row
        driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[2]/button[1]').click()

        # last step
        result = True
    except:
        result = False
    time.sleep(0.5)
    return result
        
