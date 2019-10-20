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
from tkinter import BOTH, END, LEFT, Checkbutton, IntVar, Label, ttk

from bs4 import BeautifulSoup

# Data
from reader_bfe_football import RecordedData
from strategy_laydraw import laydraw
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
        cl = 1

        # Define tabs existence
        global bet_overview
        bet_overview = ttk.Frame(tab_parent)
        def tab_overview_setup():
            tab_parent.add(bet_overview, text="Overview")
            
        tab_overview_setup() # run tab setup

        # & Bet link text

        def bet_overview_static_text():
            Label(bet_overview, text="Betfair Sportsbook URL:").grid(row=1, column = 1, columnspan = 3)
        bet_overview_static_text() # call static text

        # & Bet URL input
        global bet_url_entry
        bet_url_entry = tk.Entry(bet_overview,width = 70)
        bet_url_entry.grid(row=rw,column = cl+2, columnspan = 7, sticky="W")

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
        lay_bet_value.insert(END,"10")

        # Lay bet entry
        lay_bet_value = tk.Entry(settings,width = 20)
        lay_bet_value.grid(row=3,column = 2, sticky="W")
        lay_bet_value.insert(END,"10")


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

        # ACTION: Open Driver window and define driver variable
        try:
            # COMMENT: Case where we have already opened the window
            opened_driver = get_driver(url,url_previous)
        except:
            # COMMENT: Case where we have to open a new window
            url_previous = "not available"
            opened_driver = get_driver(url,url_previous)
       

        # ACTION: Loop through calls of functions
        for n in range(0,100000):

            # STEP: Connect to database
            conn = sqlite3.connect('bet_data.db')

            # STEP: Create a cursor object and call it for SQL commands
            c = conn.cursor()

            # STEP: Create bet data table
            try:
                c.execute("""CREATE TABLE bet_data_table (time_stamp integer,                
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

            # STEP: Parse through betfair table
            for league in range(1,6):
                for sub_table in range (1,3):
                    for row in range(1,50):
                        # STEP: Gether raw det data class (e.g. home team name)      
                        bet_data = RecordedData(league,sub_table,row,c,opened_driver.driver)

                        # STEP: Apply strategy to bet data
                        strategy_data = laydraw(bet_data,c)

                        # STEP: Check against not available
                        if bet_data.home_team_name == "not available":
                            # COMMENT: If "not available" then end row loop
                            break
                        
                        # STEP: Store define execute to send data into bet_data_table
                        c.execute("""INSERT INTO bet_data_table VALUES(:time_stamp,
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
        
            # COMMENT: print function provides feedback to user that loop is running
            print(n)

            # STEP: Close the database connection
            conn.close()

            # STEP: refresh the driver to ensure we get the latest betting data
            opened_driver.driver.refresh()

            # STEP: sleep for 1 second to allow the refreshed driver to open
            time.sleep(1)


        # ============= Tidy up ============
        # COMMENT: define url_previous to allow the existing driver to be used again
        url_previous = url


form = tk.Tk()

client = ThreadedClient(form)

form.mainloop()


