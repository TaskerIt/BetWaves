from launch_bfe_football import execute_trade

class lowodds_ct:
    def __init__(self,c,strategy):
        strategy.replace(".py","")
        try:
            c.execute(f"""CREATE TABLE {strategy} (time_stamp integer,                
            game_time_state real,
            home_team_name text,
            home_team_score integer,
            away_team_name text,
            away_team_score integer,
            favourite text,
            favourite_odds real,
            home_back_odds real,
            draw_back_odds real,
            away_back_odds real,
            market_entry_odds real,
            market_entry_type text,
            bank_volume real)""")
        except:
            # COMMENT: Except is normally triggered if table already exists - usually not a failure
            pass

class lowodds_st:
    def __init__(self,bet_data,c,conn,driver):
        
        # Configuration variables
        stake_ammount = 2
        
        # ============= Market Entry ===============
        try:
            # Check we are not already in the market
            if bet_data.previous_entry_odds == -1:
                # Check game state is at least 20 minutes before start and not in play
                if (88) < bet_data.game_time_state:
                    # home odds are less than 1.16
                    if 1.01 < bet_data.home_back_odds < 1.16:
                        # home team are winning
                        if bet_data.home_team_score > bet_data.away_team_score:
                            # PREVIOUS odds for backing home team are greater than 1.11 and less than 1.16
                            if 1.01 < bet_data.previous_home_back_odds < 1.16: # if passed -> place a bet
                                if bet_data.favourite == "home":
                                    self.market_entry_odds = bet_data.home_back_odds
                                    self.market_entry_type = "home"
                                    self.bank_volume = bet_data.previous_bank_volume - stake_ammount
                                    execute_trade(driver,bet_data.league,bet_data.sub_table,bet_data.row,"home_back",stake_ammount,bet_data.home_back_odds)
                                    print("backed: Home team - " + str(bet_data.home_team_name) + " with odds: " + str(self.market_entry_odds))
                                else:
                                    self.market_entry_odds = bet_data.previous_entry_odds
                                    self.market_entry_type = "none"
                                    self.bank_volume = bet_data.previous_bank_volume                                 
                            else:
                                self.market_entry_odds = bet_data.previous_entry_odds
                                self.market_entry_type = "none"
                                self.bank_volume = bet_data.previous_bank_volume               
                        else:
                            self.market_entry_odds = bet_data.previous_entry_odds
                            self.market_entry_type = "none"
                            self.bank_volume = bet_data.previous_bank_volume    
                    elif 1.01 < bet_data.draw_back_odds<1.16:
                        if bet_data.home_team_score == bet_data.away_team_score:
                            if 1.01 < bet_data.previous_draw_back_odds < 1.16:
                                self.market_entry_odds = bet_data.draw_back_odds
                                self.market_entry_type = "draw"
                                self.bank_volume = bet_data.previous_bank_volume - stake_ammount
                                execute_trade(driver,bet_data.league,bet_data.sub_table,bet_data.row,"draw_back",stake_ammount,bet_data.home_back_odds)
                                print("Backed: Draw in market" + str(bet_data.home_team_name) + " vs " + str(bet_data.away_team_name) + " with odds: " + str(self.market_entry_odds))
                            else:
                                self.market_entry_odds = bet_data.previous_entry_odds
                                self.market_entry_type = "none"
                                self.bank_volume = bet_data.previous_bank_volume                              
                        else:
                            self.market_entry_odds = bet_data.previous_entry_odds
                            self.market_entry_type = "none"
                            self.bank_volume = bet_data.previous_bank_volume    
                    elif 1.01 < bet_data.away_back_odds < 1.16:
                        if bet_data.home_team_score < bet_data.away_team_score:
                            if 1.01 < bet_data.previous_away_back_odds < 1.16:
                                if bet_data.favourite == "away":
                                    self.market_entry_odds = bet_data.away_back_odds
                                    self.market_entry_type = "away"
                                    self.bank_volume = bet_data.previous_bank_volume - stake_ammount
                                    execute_trade(driver,bet_data.league,bet_data.sub_table,bet_data.row,"away_back",stake_ammount,bet_data.home_back_odds)
                                    print("backed: Away team - " + str(bet_data.away_team_name) + " with odds: " + str(self.market_entry_odds))
                                else:
                                    self.market_entry_odds = bet_data.previous_entry_odds
                                    self.market_entry_type = "none"
                                    self.bank_volume = bet_data.previous_bank_volume
                            else:
                                self.market_entry_odds = bet_data.previous_entry_odds
                                self.market_entry_type = "none"
                                self.bank_volume = bet_data.previous_bank_volume
                        else:
                            self.market_entry_odds = bet_data.previous_entry_odds
                            self.market_entry_type = "none"
                            self.bank_volume = bet_data.previous_bank_volume    
                    else:
                        self.market_entry_odds = bet_data.previous_entry_odds
                        self.market_entry_type = "none"
                        self.bank_volume = bet_data.previous_bank_volume                      
                else:
                    self.market_entry_odds = bet_data.previous_entry_odds
                    self.market_entry_type = "none"
                    self.bank_volume = bet_data.previous_bank_volume
            else:
                # case where we are already in the market
                self.market_entry_odds = bet_data.previous_entry_odds
                self.bank_volume = bet_data.previous_bank_volume
                self.market_entry_type = bet_data.previous_entry_type
        except:
            self.market_entry_odds = bet_data.previous_entry_odds
            self.bank_volume = bet_data.previous_bank_volume
            self.market_entry_type = bet_data.previous_entry_type

        try:
            # Check game is finished
            if bet_data.game_time_state == 100:
                # Check we entered and exited the market
                if bet_data.previous_entry_odds > -1:
                    if bet_data.previous_entry_type == "home":
                        if bet_data.home_team_score > bet_data.away_team_score:
                            # WON
                            self.bank_volume = bet_data.previous_bank_volume + (bet_data.previous_entry_odds*stake_ammount)
                            self.market_entry_type = "won"
                        else:
                            self.bank_volume = bet_data.previous_bank_volume
                            self.market_entry_type = "lost"
                    elif bet_data.previous_entry_type == "draw":
                        if bet_data.home_team_score == bet_data.away_team_score:
                            # WON
                            self.bank_volume = bet_data.previous_bank_volume + (bet_data.previous_entry_odds*stake_ammount)
                            self.market_entry_type = "won"
                        else:
                            self.bank_volume = bet_data.previous_bank_volume
                            self.market_entry_type = "lost"
                    elif bet_data.previous_entry_type == "away":
                        if bet_data.home_team_score < bet_data.away_team_score:
                            # WON
                            self.bank_volume = bet_data.previous_bank_volume + (bet_data.previous_entry_odds*stake_ammount)
                            self.market_entry_type = "won"
                        else:
                            self.bank_volume = bet_data.previous_bank_volume
                            self.market_entry_type = "lost"
        except:
            pass


class lowodds_wt:
    def __init__(self,bet_data,c,conn, strategy_data,strategy):
        # STEP: Store define execute to send data into bet_data_table
        c.execute(f"""INSERT INTO {strategy} VALUES(:time_stamp,
        :game_time_state,
        :home_team_name,
        :home_team_score,
        :away_team_name,
        :away_team_score,
        :favourite,
        :favourite_odds,
        :home_back_odds,
        :draw_back_odds,
        :away_back_odds,
        :market_entry_odds,
        :market_entry_type,
        :bank_volume)""",{
        'time_stamp': bet_data.date,
        'game_time_state': bet_data.game_time_state, 
        'home_team_name': bet_data.home_team_name,
        'home_team_score': bet_data.home_team_score,
        'away_team_name': bet_data.away_team_name,
        'away_team_score': bet_data.away_team_score,
        'favourite':bet_data.favourite,
        'favourite_odds':bet_data.favourite_odds,
        'home_back_odds':bet_data.home_back_odds,
        'draw_back_odds':bet_data.draw_back_odds,
        'away_back_odds':bet_data.away_back_odds,
        'market_entry_odds':strategy_data.market_entry_odds, # COMMENT: Stratey specific data #1
        'market_entry_type':strategy_data.market_entry_type, # COMMENT: Stratey specific data #2
        'bank_volume':strategy_data.bank_volume}) # COMMENT: Stratey specific data #3

        # STEP: Commit data array to database
        conn.commit()##test