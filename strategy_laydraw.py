class laydraw_ct:
    def __init__(self,c,strategy):
        strategy.replace(".py","")
        try:
            c.execute(f"""CREATE TABLE {strategy} (time_stamp integer,                
            game_time_state real,
            home_team_name text,
            home_team_score integer,
            away_team_name text,
            away_team_score integer,
            total_matched real,
            home_back_odds real,
            home_back_volume real,
            home_lay_odds real,
            home_lay_volume real,
            draw_back_odds real,
            draw_back_volume real,
            draw_lay_odds real,
            draw_lay_volume real,
            away_back_odds real,
            away_back_volume real,
            away_lay_odds real,
            away_lay_volume real,
            market_entry_odds real,
            market_exit_odds real,
            bank_volume real)""")
        except:
            # COMMENT: Except is normally triggered if table already exists - usually not a failure
            pass

class laydraw_st:
    def __init__(self,bet_data,c,conn):
        
        # Configuration variables
        stake_ammount = 2
            
        # ============= Market Entry ===============
        try:
            # Check we are not already in the market
            if bet_data.previous_entry_odds == -1:
                # Check game state is at least 20 minutes before start and not in play
                if (-50) < bet_data.game_time_state:
                    if bet_data.game_time_state < 2:
                        if bet_data.count_market > 10:
                            if bet_data.total_matched > 0:
                            # condition if current draw odds are greater than average + 0.1
                                if bet_data.draw_back_odds > (bet_data.average_prev_draw_back_odds + 0.1):
                                    if bet_data.draw_back_odds > 1.1:
                                        # if current odds > average odds then enter market
                                        self.market_entry_odds = bet_data.draw_back_odds
                                        # remove money from the bank
                                        self.bank_volume = bet_data.previous_bank_volume-float(stake_ammount)
                                        print("entered - " + str(bet_data.home_team_name))
                                    else:
                                        self.market_entry_odds = -1
                                        self.bank_volume = bet_data.previous_bank_volume
                                else:
                                    self.market_entry_odds = -1
                                    self.bank_volume = bet_data.previous_bank_volume                    
                            else:
                                self.market_entry_odds = -1
                                self.bank_volume = bet_data.previous_bank_volume
                        else:
                            self.market_entry_odds = -1
                            self.bank_volume = bet_data.previous_bank_volume
                    else:
                        self.market_entry_odds = -1
                        self.bank_volume = bet_data.previous_bank_volume
                else:
                    # case where it is far before game start
                    self.market_entry_odds = -1
                    self.bank_volume = bet_data.previous_bank_volume
            else:
                # case where we are already in the market
                self.market_entry_odds = bet_data.previous_entry_odds
                # maintain bank
                self.bank_volume = bet_data.previous_bank_volume
        except:
            self.market_entry_odds = bet_data.previous_entry_odds
            # maintain bank
            self.bank_volume = bet_data.previous_bank_volume

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
                                self.bank_volume = bet_data.previous_bank_volume+stake_ammount
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
                                self.bank_volume = bet_data.previous_bank_volume+stake_ammount
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
                            self.bank_volume = bet_data.previous_bank_volume+((bet_data.previous_entry_odds-bet_data.previous_exit_odds)*stake_ammount)
                            # reset entry and exit odds to prevent further bank changes
                            self.market_entry_odds = -2
                            self.market_exit_odds = -2
                        else:
                            # stake was already returned at time of laying market
                            self.market_entry_odds = -3
                            self.market_exit_odds = -3
                    else:
                        self.bank_volume = bet_data.previous_bank_volume # do not change the entry / exit odds
                elif self.market_entry_odds > -1: # Case where we entered but did not leave
                        # check game result is draw
                    if bet_data.home_team_score == bet_data.away_team_score:
                        # game = draw then bet is won -> add winnings to bank :D
                        self.bank_volume = bet_data.previous_bank_volume+stake_ammount+(bet_data.previous_entry_odds*stake_ammount)
                        # reset entry and exit odds to prevent further bank changes
                        self.market_entry_odds = -4
                        self.market_exit_odds = -4
                    else:
                        # Case where we entered and lost out stake :(
                        self.bank_volume = bet_data.previous_bank_volume
                        self.market_entry_odds = -4
                        self.market_exit_odds = -4
                else: # Case where either a) were never in the market or b) already exited the market
                    self.bank_volume = bet_data.previous_bank_volume
        except:
            pass


class laydraw_wt:
    def __init__(self,bet_data,c,conn, strategy_data,strategy):
        # STEP: Store define execute to send data into bet_data_table
        c.execute(f"""INSERT INTO {strategy} VALUES(:time_stamp,
        :game_time_state,
        :home_team_name,
        :home_team_score,
        :away_team_name,
        :away_team_score,
        :total_matched,
        :home_back_odds,
        :home_back_volume,
        :home_lay_odds,
        :home_lay_volume,
        :draw_back_odds,
        :draw_back_volume,
        :draw_lay_odds,
        :draw_lay_volume,
        :away_back_odds,
        :away_back_volume,
        :away_lay_odds,
        :away_lay_volume,
        :market_entry_odds,
        :market_exit_odds,
        :bank_volume)""",{
        'time_stamp': bet_data.date,
        'game_time_state': bet_data.game_time_state, 
        'home_team_name': bet_data.home_team_name,
        'home_team_score': bet_data.home_team_score,
        'away_team_name': bet_data.away_team_name,
        'away_team_score': bet_data.away_team_score,
        'total_matched': bet_data.total_matched,
        'home_back_odds':bet_data.home_back_odds,
        'home_back_volume':bet_data.home_back_volume,
        'home_lay_odds':bet_data.home_lay_odds,
        'home_lay_volume':bet_data.home_lay_volume,
        'draw_back_odds':bet_data.draw_back_odds,
        'draw_back_volume':bet_data.draw_back_volume,
        'draw_lay_odds':bet_data.draw_lay_odds,
        'draw_lay_volume':bet_data.draw_lay_volume,
        'away_back_odds':bet_data.away_back_odds,
        'away_back_volume':bet_data.away_back_volume,
        'away_lay_odds': bet_data.away_lay_odds,
        'away_lay_volume':bet_data.away_lay_volume,
        'market_entry_odds':strategy_data.market_entry_odds, # COMMENT: Stratey specific data #1
        'market_exit_odds':strategy_data.market_exit_odds, # COMMENT: Stratey specific data #2
        'bank_volume':strategy_data.bank_volume}) # COMMENT: Stratey specific data #3

        # STEP: Commit data array to database
        conn.commit()