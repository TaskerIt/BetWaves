#Date
from datetime import datetime, timedelta

class RecordedData:
    def __init__(self, league,sub_table,row,c,driver):
        
        self.c = c

        try:
            self.date = datetime.today().strftime('%Y%m%d')
        except:
            self.date = 0

        self.league = league

        self.row = row

        # provide data for database
        try:
            if sub_table == 0:

                sub_table = ""
    
            else:

                sub_table = f'[{sub_table}]'
            
            # Try retrieve game_time_state while in play
            game_time_state = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/bf-livescores/section/div/div/data-bf-livescores-time-elapsed/ng-include/div/div/div').text
            self.game_time_state = self.clean_time_int(game_time_state)
        except:
            try: 
                # Try retrieve game_time_state after error - probably when not in play
                game_time_state = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/bf-livescores/section/div/div/data-bf-livescores-start-date/ng-include/div/div/span').text                                               
                self.game_time_state = self.clean_time_int(game_time_state)
            except:
                self.game_time_state = -3600
        
        try:      
            self.home_team_name = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/ul[1]/li[1]').text
        except:
            self.home_team_name = "not available"
        
        try:
            home_team_score = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/bf-livescores/section/div/div/data-bf-livescores-match-scores/ng-include/div/div/span[1]').text
            self.home_team_score = int(home_team_score)
        except:
            self.home_team_score = 0

        try:
            self.away_team_name = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/ul[1]/li[2]').text
        except:
            self.away_team_name = "not available" 

        try: 
            away_team_score = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/bf-livescores/section/div/div/data-bf-livescores-match-scores/ng-include/div/div/span[2]').text
            self.away_team_score = int(away_team_score)
        except:
            self.away_team_score = 0
        
        try:
            total_matched = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/ul[3]/li').text
            self.total_matched = self.clean_total_int(total_matched)
        except:
            self.total_matched = 0
        

        # Home back odds ---------------
        try:
            home_back_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[1]/button[1]/div/span[1]').text
            self.home_back_odds = self.clean_odds_int(home_back_odds)
        except:
            self.home_back_odds = 0
        
        # Home back volume
        try:
            home_back_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[1]/button[1]/div/span[2]').text
            self.home_back_volume = self.clean_volume_int(home_back_volume)
        except:
            self.home_back_volume = 0
        

        # Home lay odds ---------------
        try:
            home_lay_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[1]/button[2]/div/span[1]').text
            self.home_lay_odds = self.clean_odds_int(home_lay_odds)
        except:
            self.home_lay_odds = 0

        # Home lay volume
        try:
            home_lay_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[1]/button[2]/div/span[2]').text
            self.home_lay_volume = self.clean_volume_int(home_lay_volume)
        except:
            self.home_lay_volume = 0
        

        # Draw back odds ---------------
        try:
            draw_back_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[2]/button[1]/div/span[1]').text
            self.draw_back_odds = self.clean_odds_int(draw_back_odds)
        except:
            self.draw_back_odds = 0
        
        # Draw back volume
        try:
            draw_back_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[2]/button[1]/div/span[2]').text
            self.draw_back_volume = self.clean_volume_int(draw_back_volume)
        except:
            self.draw_back_volume = 0

        # Home lay odds ---------------
        try:
            draw_lay_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[2]/button[2]/div/span[1]').text
            self.draw_lay_odds = self.clean_odds_int(draw_lay_odds)
        except:
            self.draw_lay_odds = 0

        # Home lay volume
        try:            
            draw_lay_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[2]/button[2]/div/span[2]').text
            self.draw_lay_volume = self.clean_volume_int(draw_lay_volume)
        except:
            self.draw_lay_volume = 0


        # Away back odds ---------------
        try:
            away_back_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[3]/button[1]/div/span[1]').text
            self.away_back_odds = self.clean_odds_int(away_back_odds)
        except:
            self.away_back_odds = 0

        # Away back volume
        try:                
            away_back_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[3]/button[1]/div/span[2]').text
            self.away_back_volume = self.clean_volume_int(away_back_volume)
        except:
            self.away_back_volume = 0
        

        # Away lay odds ---------------
        try:
            away_lay_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[3]/button[2]/div/span[1]').text
            self.away_lay_odds = self.clean_odds_int(away_lay_odds)
        except:
            self.away_lay_odds = 0

        # Away lay volume
        try:
            away_lay_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table{sub_table}/div/table/tbody/tr[{row}]/td[2]/div[3]/button[2]/div/span[2]').text
            self.away_lay_volume = self.clean_volume_int(away_lay_volume)
        except:
            self.away_lay_volume = 0

        # previous exit odds
        try:
            self.previous_exit_odds = self.check_market("market_exit_odds",c)
        except:
            self.previous_exit_odds = -1
        
        # previous entry odds
        try:
            self.previous_entry_odds = self.check_market("market_entry_odds",c)
        except:
            self.previous_entry_odds = -1

    def check_market(self,selecter,c):
        # Define WHERE conditions according to SQLite3 protocol with following array -> improtant is the final comma
        t = (self.date, self.home_team_name,self.away_team_name,)
        # try to break on error
        try:
            # execute the SQLite3 Query including where with same timestamp, home team name and away team name
            c.execute(f'SELECT {selecter} FROM bet_data_table WHERE time_stamp = ? AND home_team_name = ? AND away_team_name = ? ORDER BY rowid DESC LIMIT 1',t)
            # fetch above query including limit 1 - result is either an array or None
            last_row = c.fetchone()
            # Check number 1 if last row is empty - check for data yesterday
            if last_row is None:
                # calculate yesterdays date
                yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y%m%d')
                # execute the SQLite3 Query including where with yesterdays timestamp, home team name and away team name
                t = (yesterday_date, self.home_team_name,self.away_team_name,)
                # Query for a match yesterday
                c.execute(f'SELECT {selecter} FROM bet_data_table WHERE time_stamp = ? AND home_team_name = ? AND away_team_name = ? ORDER BY rowid DESC LIMIT 1',t)
                # fetch above query including limit 1
                last_row = c.fetchone()
            # Check number 2 for if the last row is still empty
            if last_row is None:
                # Assign data as -1 to show no previous data available
                data = -1
            else:
                # Else get data from first item in list of last row
                data = last_row[0]
        except:
            # exception in case of error - assume we have not entered the market
            data = -1    
        return data   

    def clean_volume_int(self,data):
        data = str(data)
        data = data.replace(" ","")
        data = data.replace("€","")
        data = data.replace("£","")
        data = float(data)
        return data

    def clean_time_int(self,data):
        #data = str(data)
        try:
            if data.find('Starting in ') != -1: # Game starting in
                # remove starting in with negative
                data = data.replace("Starting in ","-")
                data = data.replace("'","")
            elif data.find('Starting soon') != -1: # Game starting soon
                data = -0.5
            elif data.find('Today ') != -1: # Game starting today
                data = data.replace("Today ","")
                data_hour = int(data[:2])
                data_min = int(data[-2:])
                now_hour = int(datetime.today().strftime('%H'))
                now_min = int(datetime.today().strftime('%M'))
                data = str(-(60*(data_hour - now_hour) + (data_min - now_min)))
            elif data.find('HT') != -1:
                data = 45.5
            elif data.find('END') != -1:
                data = 100
            else: # Normal case for time
                data = data.replace("'","")
        except:
            pass
        data = float(data) # convert to float for storage
        return data

    def clean_total_int(self,data):
        data = str(data)
        data = data.replace(" ","")
        data = data.replace("€","")
        data = data.replace("£","")
        data = data.replace(",","")
        data = float(data)
        return data

    def clean_odds_int(self,data):
        data = str(data)
        data = data.replace(" ","")
        data = data.replace("€","")
        data = data.replace("£","")
        data = float(data)
        return data