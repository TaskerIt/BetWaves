#import tkinter
import queue
# SQL
import sqlite3
import threading
# Functionality
import time
# tkinter GUI
import tkinter as tk
#Date
from datetime import datetime, timedelta
from tkinter import BOTH, END, LEFT, Checkbutton, IntVar, Label, ttk, Tk, OptionMenu, StringVar, messagebox
# BeautifulSoup
from bs4 import BeautifulSoup
# System
import sys
# Data
from reader_bfe_football import RecordedData
from strategy_laydraw import laydraw_ct, laydraw_st, laydraw_wt
from strategy_lowodds import lowodds_ct, lowodds_st, lowodds_wt
from strategy_lowodds_backlay import lowodds_backlay_ct, lowodds_backlay_st, lowodds_backlay_wt
from open_driver import get_driver

class GuiPart:
    def __init__(self, master, queue, scrape_url):
        self.queue = queue

        # ACTION: 

        def form_setup(): # function to combin form setup
            form.iconbitmap('Wave_inputs/wave_ico.ico')# Assign icon
            form.title("Betfair Wave")# Assign window titly
        form_setup() # run form setup
    
        # Define parent tab
        tab_parent = ttk.Notebook(form)

        # ------------------- Bet overview tab
        # init constants 
        rw = 1

        # Define tabs existence
        global bet_overview
        bet_overview = ttk.Frame(tab_parent)
        def tab_overview_setup():
            tab_parent.add(bet_overview, text="Overview")
            
        tab_overview_setup() # run tab setup

        # & Bet link text
        
        def bet_overview_static_text():
            Label(bet_overview, text="Betfair Sportsbook URL: ").grid(row=1, column = 1, columnspan = 1)
            Label(bet_overview, text="Strategy: ").grid(row=2, column = 1, columnspan = 1)
            Label(bet_overview, text="TIme period (s): ").grid(row=3, column = 1, columnspan = 1)

        bet_overview_static_text() # call static text

        # & Bet URL input
        global bet_url_entry
        bet_url_entry = tk.Entry(bet_overview,width = 70)
        bet_url_entry.grid(row=rw,column = 3, columnspan = 7, sticky="W")
        bet_url_entry.insert(END,"https://www.betfair.com/exchange/plus/football")


        # Strategy drop down menu
        OPTIONS = []
        import os
        for file in os.listdir():
            if file.startswith("strategy"):
                file = file.replace(".py","")
                OPTIONS.append(file)

        global strategyoptions
        strategyoptions = StringVar(bet_overview)
        strategyoptions.set(OPTIONS[1]) # default value
        
        w = OptionMenu(bet_overview, strategyoptions, *OPTIONS)
        w.grid(row=2, column = 3, columnspan = 1)

        # Timer drop down menu
        timeoptions = [60,600,6000,6000]

        global timeoption
        timeoption = StringVar(bet_overview)
        timeoption.set(timeoptions[3]) # default value

        w = OptionMenu(bet_overview, timeoption, *timeoptions)
        w.grid(row=3, column = 3, columnspan = 1)

        #w.pack()


        # & Start button

        start_btn_scrape = tk.Button(bet_overview, text ="Start", command = scrape_url, width = 15)
        start_btn_scrape.grid(row=rw,column = 10, sticky="W")

        # ------------------- Settings
        # init constants 
        srw = 1

        # -------- Define tabs existence
        settings = ttk.Frame(tab_parent)
        def tab_settings_setup():
            tab_parent.add(settings, text="Settings")
        tab_settings_setup() # run tab setup

        # Lift tkinter to front
        var1 = IntVar()

        def on_top_func():
            if var1.get() == 1:
                form.lift()
                form.call('wm', 'attributes', '.', '-topmost', '1')
            else:
                form.call('wm', 'attributes', '.', '-topmost', '0')

        Checkbutton(settings, text="Window always visible", variable=var1, command = on_top_func).grid(row=srw, sticky="W", columnspan = 3)
        

        # Add text
        def settings_static_text():
            Label(settings, text="Back Bet Value:").grid(row=2, column =1, sticky="W")
            Label(settings, text="Lay Bet Value:").grid(row=3, column =1, sticky="W")
            
        settings_static_text() # call static text

        # Lay bet entry
        lay_bet_value = tk.Entry(settings,width = 20)
        lay_bet_value.grid(row=2,column = 2, sticky="W")
        lay_bet_value.insert(END,"2")

        # Lay bet entry
        lay_bet_value = tk.Entry(settings,width = 20)
        lay_bet_value.grid(row=3,column = 2, sticky="W")
        lay_bet_value.insert(END,"2")


        # unpack tabs
        tab_parent.pack(expand=1,fill="both")
        # main loop
        # Add more GUI stuff here depending on your specific needs

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                # Check contents of message and do whatever is needed. As a
                # simple test, print it (in real life, you would
                # suitably update the GUI's display in a richer fashion).
                print(msg)
            except queue.Empty:
                # just on general principles, although we don't
                # expect this branch to be taken in this case
                pass

# Execute trade


class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.scrape_url)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        #self.thread1.start(  )

        #self.thread2 = threading.Thread(target=self.scrape_url)

        #self.thread2.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall(  )

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(  )
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            #sys.exit()
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            #time.sleep(rand.random() * 1.5)
            #msg = rand.random()
            #self.queue.put(msg)
            pass

    def endApplication(self):
        while self.running:
            print("hello")
        #self.running = 0
    
    def scrape_url(self):

        # ACTION: Define variables
        global opened_driver
        global url_previous

        # ACTION: Retrieve URL from Tkinter text window
        url = bet_url_entry.get()
        strategy = strategyoptions.get()
        timelimit = int(timeoption.get())
        # ACTION: Open Driver window and define driver variable
        try:
            # COMMENT: Case where we have already opened the window
            opened_driver = get_driver(url)
        except:
            # COMMENT: Case where we have to open a new window
            messagebox.showerror("Error opening driver", "Exiting Program")
            # COMMENT: 
            sys.exit()
       
        print("Macro started")

        # ACTION: Loop through calls of functions
        time_elapsed = 0
        start_time = time.time()

        # STEP: Connect to database
        conn = sqlite3.connect('bet_data.db')

        # STEP: Create a cursor object and call it for SQL commands
        c = conn.cursor()

        # STEP: Create strategy specific table
        if strategy == "strategy_laydraw":
            # STEP: create table
            laydraw_ct(c,strategy)
            # Define max value + 1
            max_league = 5
            max_subtable = 5
            max_row = 50
        elif strategy == "strategy_lowodds":
            lowodds_ct(c,strategy)
            # Define max value + 1
            max_league = 2
            max_subtable = 3
            max_row = 11
            # STEP: Define dictionary:
            strategy_lowodds_readstates = {
            "time_stamp":"yes",                
            "game_time_state":"yes" ,
            "home_team_name":"yes" ,
            "home_team_score":"yes" ,
            "away_team_name":"yes" ,
            "away_team_score":"yes" ,
            "favourite":"yes",
            "favourite text":"yes",
            "favourite_odds":"yes" ,
            "total_matched":"no" ,
            "home_back_odds":"yes" ,
            "previous_home_back_odds":"yes",
            "average_prev_home_back_odds":"yes",
            "home_back_volume":"no",
            "home_lay_odds":"no",
            "average_prev_home_lay_odds":"yes",
            "home_lay_volume":"no" ,
            "draw_back_odds":"yes" ,
            "previous_draw_back_odds":"yes",
            "average_prev_draw_back_odds":"yes",
            "draw_back_volume":"no" ,
            "draw_lay_odds":"no" ,
            "average_prev_draw_lay_odds":"yes",
            "draw_lay_volume":"no" ,
            "away_back_odds":"yes" ,
            "previous_away_back_odds":"yes",
            "average_prev_away_back_odds":"yes",
            "away_back_volume":"no" ,
            "away_lay_odds":"no" ,
            "away_lay_volume":"no" ,
            "previous_entry_type":"yes",
            "market_entry_odds":"yes" ,
            "previous_entry_odds": "yes",
            "market_exit_odds":"yes" ,
            "previous_bank_volume":"yes",
            "bank_volume":"yes",
            "count_market":"yes"
            }
        elif strategy == "strategy_lowodds_backlay":
            lowodds_backlay_ct(c,strategy)
            # Define max value + 1
            max_league = 2
            max_subtable = 3
            max_row = 11
            # STEP: Define dictionary:
            strategy_lowodds_readstates = {
            "time_stamp":"yes",                
            "game_time_state":"yes" ,
            "home_team_name":"yes" ,
            "home_team_score":"yes" ,
            "away_team_name":"yes" ,
            "away_team_score":"yes" ,
            "favourite":"yes",
            "favourite text":"yes",
            "favourite_odds":"yes" ,
            "total_matched":"no" ,
            "home_back_odds":"yes" ,
            "previous_home_back_odds":"yes",
            "average_prev_home_back_odds":"yes",
            "home_back_volume":"no",
            "home_lay_odds":"no",
            "average_prev_home_lay_odds":"yes",
            "home_lay_volume":"no" ,
            "draw_back_odds":"yes" ,
            "previous_draw_back_odds":"yes",
            "average_prev_draw_back_odds":"yes",
            "draw_back_volume":"no" ,
            "draw_lay_odds":"no" ,
            "average_prev_draw_lay_odds":"yes",
            "draw_lay_volume":"no" ,
            "away_back_odds":"yes" ,
            "previous_away_back_odds":"yes",
            "average_prev_away_back_odds":"yes",
            "away_back_volume":"no" ,
            "away_lay_odds":"no" ,
            "away_lay_volume":"no" ,
            "previous_entry_type":"yes",
            "market_entry_odds":"yes" ,
            "previous_entry_odds": "yes",
            "market_exit_odds":"yes" ,
            "previous_bank_volume":"yes",
            "bank_volume":"yes",
            "count_market":"yes"
            }



        while time_elapsed <= timelimit:
            # STEP: Parse through betfair table
            for league in range(1,max_league):
                for sub_table in range (1,max_subtable):
                    for row in range(1,max_row):                        
                        if strategy == "strategy_laydraw":
                            # STEP: Gether raw det data class (e.g. home team name)      
                            bet_data = RecordedData(league,sub_table,row,c,opened_driver.driver,strategy,strategy_lowodds_readstates)
                            # STEP: Check against not available
                            if bet_data.home_team_name == "not available":
                                # COMMENT: If "not available" then end row loop
                                break
                            # STEP: Apply strategy to bet data
                            strategy_data = laydraw_st(bet_data,c,conn)
                            # STEP: Write results to table
                            laydraw_wt(bet_data,c,conn,strategy_data,strategy)
                        elif strategy == "strategy_lowodds":
                            # STEP: Gether raw det data class (e.g. home team name)      
                            bet_data = RecordedData(league,sub_table,row,c,opened_driver.driver,strategy,strategy_lowodds_readstates)
                            # STEP: Check against not available
                            if bet_data.home_team_name == "not available":
                                # COMMENT: If "not available" then end row loop
                                break
                            # STEP: Apply strategy to bet data
                            strategy_data = lowodds_st(bet_data,c,conn,opened_driver.driver)
                            # STEP: Write results to table
                            lowodds_wt(bet_data,c,conn,strategy_data,strategy)

                            if bet_data.previous_entry_type == "none" and strategy_data.market_entry_type != "none":
                                break
                        elif strategy == "strategy_lowodds_backlay":
                            # STEP: Gether raw det data class (e.g. home team name)      
                            bet_data = RecordedData(league,sub_table,row,c,opened_driver.driver,strategy,strategy_lowodds_readstates)
                            # STEP: Check against not available
                            if bet_data.home_team_name == "not available":
                                # COMMENT: If "not available" then end row loop
                                break
                            # STEP: Apply strategy to bet data
                            strategy_data = lowodds_backlay_st(bet_data,c,conn,opened_driver.driver)
                            # STEP: Write results to table
                            lowodds_backlay_wt(bet_data,c,conn,strategy_data,strategy)

                            if bet_data.previous_entry_type == "none" and strategy_data.market_entry_type != "none":
                                break
            # STEP: Increment time elapsed
            time_elapsed = time.time() - start_time
            print(str(time_elapsed)+"s - cycle completed")
            # COMMENT: print function provides feedback to user that loop is running

        # STEP: Close the database connection
        conn.close()


        
        print("Macro finished")

        # ============= Tidy up ============
        # COMMENT: define url_previous to allow the existing driver to be used again
        url_previous = url


form = tk.Tk()

client = ThreadedClient(form)

form.mainloop()


