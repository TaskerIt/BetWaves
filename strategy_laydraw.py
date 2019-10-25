class laydraw:
    def __init__(self,bet_data,c):
        
        # Configuration variables
        stake_ammount = 2
        
        # previous bank volume
        try:
            self.previous_bank_volume = self.get_bank_volume(c)
        except:
            self.previous_bank_volume = 0

        # average draw odds

        try:
            self.average_draw_back_odds = self.average_data_datehtat("draw_back_odds",bet_data,c)
        except:
            self.average_draw_back_odds = 10000 # failure case

        try:
            t = (bet_data.date, bet_data.home_team_name,bet_data.away_team_name,)
            c.execute(f'SELECT COUNT(*) FROM bet_data_table WHERE time_stamp = ? AND home_team_name = ? AND away_team_name = ?',t)
            # fetch last value and store in array
            result = c.fetchone()
            self.number_rows = result[0]
        except:
            self.number_rows = 0
            
        # ============= Market Entry ===============
        try:
            # Check we are not already in the market
            if bet_data.previous_entry_odds == -1:
                # Check game state is at least 20 minutes before start and not in play
                if (-50) < bet_data.game_time_state:
                    if bet_data.game_time_state < 2:
                        if self.number_rows > 10:
                            if bet_data.total_matched > 0:
                            # condition if current draw odds are greater than average + 0.1
                                if bet_data.draw_back_odds > (self.average_draw_back_odds + 0.1):
                                    if bet_data.draw_back_odds > 1.1:
                                        # if current odds > average odds then enter market
                                        self.market_entry_odds = bet_data.draw_back_odds
                                        # remove money from the bank
                                        self.bank_volume = self.previous_bank_volume-float(stake_ammount)
                                        print("entered - " + str(bet_data.home_team_name))
                                    else:
                                        self.market_entry_odds = -1
                                        self.bank_volume = self.previous_bank_volume
                                else:
                                    self.market_entry_odds = -1
                                    self.bank_volume = self.previous_bank_volume                    
                            else:
                                self.market_entry_odds = -1
                                self.bank_volume = self.previous_bank_volume
                        else:
                            self.market_entry_odds = -1
                            self.bank_volume = self.previous_bank_volume
                    else:
                        self.market_entry_odds = -1
                        self.bank_volume = self.previous_bank_volume
                else:
                    # case where it is far before game start
                    self.market_entry_odds = -1
                    self.bank_volume = self.previous_bank_volume
            else:
                # case where we are already in the market
                self.market_entry_odds = bet_data.previous_entry_odds
                # maintain bank
                self.bank_volume = self.previous_bank_volume
        except:
            self.market_entry_odds = bet_data.previous_entry_odds
            # maintain bank
            self.bank_volume = self.previous_bank_volume

        # Market Exit odds
        margin = 0.1
        try:
            # Check we are currently in the market
            if self.market_entry_odds != -1:
                if bet_data.previous_exit_odds == -1:
                # Check game state is in_play
                    if bet_data.game_time_state > (0): # prematch
                        # enter market if 0 < current draw odds <= market entry odds
                        if 0<bet_data.draw_lay_odds:
                            if bet_data.draw_lay_odds<=(bet_data.previous_entry_odds-margin):
                                # exit market at lay odds
                                self.market_exit_odds = bet_data.draw_lay_odds
                                # return stake as we have now left the market
                                self.bank_volume = self.previous_bank_volume+stake_ammount
                                # reset entry and exit odds to prevent further bank changes
                                print("exited - " + str(bet_data.home_team_name))
                            else:
                                self.market_exit_odds = -1
                        else:
                            self.market_exit_odds = -1
                    else: # in play
                        # enter market if 0 < current draw odds <= market entry odds
                        if 0<bet_data.draw_lay_odds:
                            if bet_data.draw_lay_odds<=(bet_data.previous_entry_odds-margin):
                                # exit market at lay odds
                                self.market_exit_odds = bet_data.draw_lay_odds
                                # return stake as we have now left the market
                                self.bank_volume = self.previous_bank_volume+stake_ammount
                                print("exited - " + str(bet_data.home_team_name))
                            else:
                                self.market_exit_odds = -1
                        else:
                            self.market_exit_odds = -1
                else:
                    # case where we are already out of the market
                    self.market_exit_odds = bet_data.previous_exit_odds
            else:
                # case where we are already out of the market
                self.market_exit_odds = bet_data.previous_exit_odds
        except:
            self.market_exit_odds = bet_data.previous_exit_odds

        try:
            # Check game is finished
            if bet_data.game_time_state == 100:
                # Check we entered and exited the market
                if bet_data.previous_entry_odds > -1:
                    if bet_data.previous_exit_odds > -1:
                        # check game result is draw
                        if bet_data.home_team_score == bet_data.away_team_score:
                            # game = draw then bet is won -> add winnings to bank
                            self.bank_volume = self.previous_bank_volume+((bet_data.previous_entry_odds-bet_data.previous_exit_odds)*stake_ammount)
                            # reset entry and exit odds to prevent further bank changes
                            self.market_entry_odds = -2
                            self.market_exit_odds = -2
                        else:
                            # stake was already returned at time of laying market
                            self.market_entry_odds = -3
                            self.market_exit_odds = -3
                    else:
                        self.bank_volume = self.previous_bank_volume # do not change the entry / exit odds
                elif self.market_entry_odds > -1: # Case where we entered but did not leave
                        # check game result is draw
                    if bet_data.home_team_score == bet_data.away_team_score:
                        # game = draw then bet is won -> add winnings to bank :D
                        self.bank_volume = self.previous_bank_volume+stake_ammount+(bet_data.previous_entry_odds*stake_ammount)
                        # reset entry and exit odds to prevent further bank changes
                        self.market_entry_odds = -4
                        self.market_exit_odds = -4
                    else:
                        # Case where we entered and lost out stake :(
                        self.bank_volume = self.previous_bank_volume
                        self.market_entry_odds = -4
                        self.market_exit_odds = -4
                else: # Case where either a) were never in the market or b) already exited the market
                    self.bank_volume = self.previous_bank_volume
        except:
            pass


    def get_bank_volume(self,c):
        # try to break on error
        try:
            # execute the SQLite3 Query for bank volumne list
            c.execute(f'SELECT bank_volume FROM bet_data_table ORDER BY rowid DESC LIMIT 1')
            # fetch last value and store in array
            last_row = c.fetchone()
            # Check last row is not empty
            if last_row is not None:
                # get last row value
                current_bank = last_row[0]
            else:
                # if no rows found assume bank = 0
                current_bank = 0
        except:
            # in case of failure assume bank = 0
            current_bank = 0
        return current_bank

    def average_data_datehtat(self,selecter,bet_data,c):
        # Define WHERE conditions according to SQLite3 protocol with following array -> improtant is the final comma
        t = (bet_data.date, bet_data.home_team_name,bet_data.away_team_name,)
        # data variable
        data = 0
        # try to break on error
        try:
            # execute the SQLite3 Query including where with same timestamp, home team name and away team name
            c.execute(f'SELECT {selecter} FROM bet_data_table WHERE time_stamp = ? AND home_team_name = ? AND away_team_name = ?',t)
            # fetch all selected values and store in array
            rows = c.fetchall()
            # calculate sum total over array
            for row in rows:
                # sum
                data += row[0]
            # calculate mean average value
            if len(rows)>0:
                data = data / len(rows)
            else:
                data = 10000 # failure case
        except:
            # exception in case of error
            if selecter == "draw_back_odds":
                data = bet_data.draw_back_odds
            else:
                data = 10000 # failure case
        return data