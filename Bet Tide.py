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
from datetime import datetime
from tkinter import BOTH, END, LEFT, Checkbutton, IntVar, Label, ttk

from bs4 import BeautifulSoup
# Beautiful Soup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class GuiPart:
    def __init__(self, master, queue, scrape_url, clear_selection, enter_market, exit_market):
        self.queue = queue

        # Set up the GUI

        def form_setup(): # function to combin form setup
            form.iconbitmap('wave_ico.ico')# Assign icon
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

        # Clear Selection button

        start_btn_scrape = tk.Button(bet_overview, text ="Clear Selection", command = clear_selection, width = 15)
        start_btn_scrape.grid(row=rw +1 ,column = 10, sticky="W")

        # Enter market button

        start_btn_scrape = tk.Button(bet_overview, text ="Enter", command = enter_market, width = 15)
        start_btn_scrape.grid(row=rw +2 ,column = 10, sticky="W")

        # Exit market button

        start_btn_scrape = tk.Button(bet_overview, text ="Exit", command = exit_market, width = 15)
        start_btn_scrape.grid(row=rw +3 ,column = 10, sticky="W")

        # output array


        tree_height = 6
        column_width = 80

        global tree_h
        global tree_a
        global tree_d
        tree_h = ttk.Treeview(bet_overview, height=tree_height)
        tree_a = ttk.Treeview(bet_overview, height=tree_height)
        tree_d = ttk.Treeview(bet_overview, height=tree_height)

        tree_h["columns"] = ("equity")
        tree_a["columns"] = ("equity")
        tree_d["columns"] = ("equity")

        tree_h.column('#0', width=column_width)
        tree_a.column('#0', width=column_width)
        tree_d.column('#0', width=column_width)

        tree_h.column('equity', width=column_width)
        tree_a.column('equity', width=column_width)
        tree_d.column('equity', width=column_width)

        tree_h.heading("#0",text="Home Odds",anchor=tk.W)
        tree_a.heading("#0",text="Away Odds",anchor=tk.W)
        tree_d.heading("#0",text="Draw Odds",anchor=tk.W)

        tree_h.heading("equity", text="Total Equity",anchor=tk.W)
        tree_a.heading("equity", text="Total Equity",anchor=tk.W)
        tree_d.heading("equity", text="Total Equity",anchor=tk.W)

        # insert row - home
        tree_h.insert("", 'end', 'h_b1_t', text = "b1", values = 0) # insert item 1
        tree_h.insert("", 'end', 'h_b2_t', text = "b2", values = 0, tags=('t_b2')) # insert item 1
        tree_h.insert("", 'end', 'h_b3_t', text = "b3", values = 0, tags=('t_b3')) # insert item 1
        tree_h.insert("", 'end', 'h_l1_t', text = "l1", values = 0, tags=('t_l1')) # insert item 1
        tree_h.insert("", 'end', 'h_l2_t', text = "l2", values = 0, tags=('t_l2')) # insert item 1
        tree_h.insert("", 'end', 'h_l3_t', text = "l3", values = 0) # insert item 1

        tree_a.insert("", 'end', 'a_b1_t', text = "", values = 0) # insert item 1
        tree_a.insert("", 'end', 'a_b2_t', text = "", values = 0, tags=('t_b2')) # insert item 1
        tree_a.insert("", 'end', 'a_b3_t', text = "", values = 0, tags=('t_b3')) # insert item 1
        tree_a.insert("", 'end', 'a_l1_t', text = "", values = 0, tags=('t_l1')) # insert item 1
        tree_a.insert("", 'end', 'a_l2_t', text = "", values = 0, tags=('t_l2')) # insert item 1
        tree_a.insert("", 'end', 'a_l3_t', text = "", values = 0) # insert item 1

        tree_d.insert("", 'end', 'd_b1_t', text = "", values = 0) # insert item 1
        tree_d.insert("", 'end', 'd_b2_t', text = "", values = 0, tags=('t_b2')) # insert item 1
        tree_d.insert("", 'end', 'd_b3_t', text = "", values = 0, tags=('t_b3')) # insert item 1
        tree_d.insert("", 'end', 'd_l1_t', text = "", values = 0, tags=('t_l1')) # insert item 1
        tree_d.insert("", 'end', 'd_l2_t', text = "", values = 0, tags=('t_l2')) # insert item 1
        tree_d.insert("", 'end', 'd_l3_t', text = "", values = 0) # insert item 1

        tree_h.tag_configure("t_b3", background='steelblue1')
        tree_h.tag_configure("t_l1", background='hotpink1')
        tree_h.tag_configure("t_b2", background='lightblue1')
        tree_h.tag_configure("t_l2", background='pink1')

        tree_a.tag_configure("t_b3", background='steelblue1')
        tree_a.tag_configure("t_l1", background='hotpink1')
        tree_a.tag_configure("t_b2", background='lightblue1')
        tree_a.tag_configure("t_l2", background='pink1')

        tree_d.tag_configure("t_b3", background='steelblue1')
        tree_d.tag_configure("t_l1", background='hotpink1')
        tree_d.tag_configure("t_b2", background='lightblue1')
        tree_d.tag_configure("t_l2", background='pink1')

        tree_h.grid(row=5,column = 2,pady=0, padx=10, rowspan = 7, sticky="W")
        tree_a.grid(row=5,column = 5,pady=0, padx=10, rowspan = 7, sticky="W")
        tree_d.grid(row=5,column = 8,pady=0, padx=10, rowspan = 7, sticky="W")

        # labels:
        x = tree_h.get_children()

        # ------------------- Settings
        # init constants 
        srw = 1
        scl = 1

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

        on_top = Checkbutton(settings, text="Window always visible", variable=var1, command = on_top_func).grid(row=srw, sticky="W", columnspan = 3)
        on_top_func()

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

class RecordedData:
    def __init__(self, league,row):

        try:
            self.date = datetime.today().strftime('%Y%m%d%H%M%S')
        except:
            self.date = 0

        # provide data for database
        try:
            self.game_time_state = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table[1]/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/bf-livescores/section/div/div/data-bf-livescores-time-elapsed/ng-include/div/div/div').text
        except:
            self.game_time_state = -1
        
        try:
            self.home_team_name = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/ul[1]/li[1]').text
        except:
            self.home_team_name = "not available"

        try:
            home_team_score = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table[1]/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/bf-livescores/section/div/div/data-bf-livescores-match-scores/ng-include/div/div/span[1]').text
            self.home_team_score = int(home_team_score)
        except:
            self.home_team_score = 0

        try:
            self.away_team_name = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/ul[1]/li[2]').text
        except:
            self.away_team_name = "not available" 

        try: 
            away_team_score = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table[1]/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/bf-livescores/section/div/div/data-bf-livescores-match-scores/ng-include/div/div/span[2]').text
            self.away_team_score = int(away_team_score)
        except:
            self.away_team_score = 0
        
        try:
            total_matched = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[1]/a/event-line/section/ul[3]/li').text
            self.total_matched = self.clean_total_int(total_matched)
        except:
            self.total_matched = 0
        

        # Home back odds ---------------
        try:
            home_back_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[1]/button[1]/div/span[1]').text
            self.home_back_odds = self.clean_odds_int(home_back_odds)
        except:
            self.home_back_odds = 0
        
        # Home back volume
        try:
            home_back_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[1]/button[1]/div/span[2]').text
            self.home_back_volume = self.clean_volume_int(home_back_volume)
        except:
            self.home_back_volume = 0
        

        # Home lay odds ---------------
        try:
            home_lay_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[1]/button[2]/div/span[1]').text
            self.home_lay_odds = self.clean_odds_int(home_lay_odds)
        except:
            self.home_lay_odds = 0

        # Home lay volume
        try:
            home_lay_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[1]/button[2]/div/span[2]').text
            self.home_lay_volume = self.clean_volume_int(home_lay_volume)
        except:
            self.home_lay_volume = 0
        

        # Draw back odds ---------------
        try:
            draw_back_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[2]/button[1]/div/span[1]').text
            self.draw_back_odds = self.clean_odds_int(draw_back_odds)
        except:
            self.draw_back_odds = 0
        
        # Draw back volume
        try:
            draw_back_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[2]/button[1]/div/span[2]').text
            self.draw_back_volume = self.clean_volume_int(draw_back_volume)
        except:
            self.draw_back_volume = 0

        # Home lay odds ---------------
        try:
            draw_lay_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[2]/button[2]/div/span[1]').text
            self.draw_lay_odds = self.clean_odds_int(draw_lay_odds)
        except:
            self.draw_lay_odds = 0

        # Home lay volume
        try:            
            draw_lay_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[2]/button[2]/div/span[2]').text
            self.draw_lay_volume = self.clean_volume_int(draw_lay_volume)
        except:
            self.draw_lay_volume = 0


        # Away back odds ---------------
        try:
            away_back_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[3]/button[1]/div/span[1]').text
            self.away_back_odds = self.clean_odds_int(away_back_odds)
        except:
            self.away_back_odds = 0

        # Away back volume
        try:                
            away_back_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[3]/button[1]/div/span[2]').text
            self.away_back_volume = self.clean_volume_int(away_back_volume)
        except:
            self.away_back_volume = 0
        

        # Away lay odds ---------------
        try:
            away_lay_odds = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[3]/button[2]/div/span[1]').text
            self.away_lay_odds = self.clean_odds_int(away_lay_odds)
        except:
            self.away_lay_odds = 0

        # Away lay volume
        try:
            away_lay_volume = driver.find_element_by_xpath(f'//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div/div/div[1]/div/div[1]/bf-super-coupon/main/ng-include[3]/section[{league}]/div[2]/bf-coupon-table/div/table/tbody/tr[{row}]/td[2]/div[3]/button[2]/div/span[2]').text
            self.away_lay_volume = self.clean_volume_int(away_lay_volume)
        except:
            self.away_lay_volume = 0

        # Insert data to database
    def clean_volume_int(self,data):
        data = str(data)
        data = data.replace(" ","")
        data = data.replace("€","")
        data = data.replace("£","")
        data = float(data)
        return data

    def clean_total_int(self,data):
        data = str(data)
        data = data.replace(" ","")
        data = data.replace("€","")
        data = data.replace("£","")
        return data

    def clean_odds_int(self,data):
        data = str(data)
        data = data.replace(" ","")
        data = data.replace("€","")
        data = data.replace("£","")
        data = float(data)
        return data


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
        self.gui = GuiPart(master, self.queue, self.scrape_url, self.clear_selection, self.enter_market,self.exit_market)

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
        #while self.running:
        # retireve bet URL from input text
        global driver
        global url_previous
        url = bet_url_entry.get()
        # start chrom driver
        if url != "": # check box filled
            try:
                if url == url_previous:
                    # case when matching -> repeat run
                    n_finish = 20
                else:
                    driver.get(url)
                    time.sleep(2)
                    url_previous = url
                    n_finish = 1
                    # case when url previous exists
            except:
                driver = webdriver.Chrome(executable_path=r"Wave_inputs/Chromedriver.exe")
                driver.get(url)
                time.sleep(2)
                url_previous = url
                n_finish = 1

            n = 0

            while n < 100000:
                self.queue.put(self.record_football_data(driver))
                print(n)
                driver.refresh()
                time.sleep(1)
                n = n + 1

        return driver
            
        print("w8")

    #====================== Algorithym code #1 =====================

    def get_market_data(self,driver):
        # define constants
        home = 1
        away = 2
        draw = 3
        b1 = 0
        b2 = 1
        b3 = 2
        l3 = 3
        l2 = 4
        l1 = 5
        # init data array

        # define xpaths

        # team names
        h_tn_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[1]/div/div[2]/mv-runner-info/div/div/h3'
        a_tn_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[1]/div/div[2]/mv-runner-info/div/div/h3'
        d_tn_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[1]/div/div[2]/mv-runner-info/div/div/h3'

        # home team - back
        h_b1_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[2]/button/div/span[1]'
        h_b1_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[2]/button/div/span[2]'
        h_b2_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[3]/button/div/span[1]'
        h_b2_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[3]/button/div/span[2]'
        h_b3_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[4]/button/div/span[1]'
        h_b3_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[4]/button/div/span[2]'
        # home team - lay
        h_l1_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[5]/button/div/span[1]'
        h_l1_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[5]/button/div/span[2]'
        h_l2_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[6]/button/div/span[1]'
        h_l2_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[6]/button/div/span[2]'
        h_l3_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[7]/button/div/span[1]'
        h_l3_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[1]/td[7]/button/div/span[2]'
        
        # away team - back
        a_b1_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[2]/button/div/span[1]'
        a_b1_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[2]/button/div/span[2]'
        a_b2_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[3]/button/div/span[1]'
        a_b2_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[3]/button/div/span[2]'
        a_b3_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[4]/button/div/span[1]'
        a_b3_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[4]/button/div/span[2]'
        # away team - lay
        a_l1_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[5]/button/div/span[1]'
        a_l1_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[5]/button/div/span[2]'
        a_l2_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[6]/button/div/span[1]'
        a_l2_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[6]/button/div/span[2]'
        a_l3_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[7]/button/div/span[1]'
        a_l3_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[{row}]/td[7]/button/div/span[2]'
    
        # draw - back
        d_b1_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[2]/button/div/span[1]'
        d_b1_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[2]/button/div/span[2]'
        d_b2_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[3]/button/div/span[1]'
        d_b2_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[3]/button/div/span[2]'
        d_b3_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[4]/button/div/span[1]'
        d_b3_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[4]/button/div/span[2]'
        # draw team - lay
        d_l1_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[5]/button/div/span[1]'
        d_l1_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[5]/button/div/span[2]'
        d_l2_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[6]/button/div/span[1]'
        d_l2_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[6]/button/div/span[2]'
        d_l3_o_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[7]/button/div/span[1]'
        d_l3_c_xp = '//*[@id="main-wrapper"]/div/div[2]/div/ui-view/div/div/div[1]/div[3]/div/div[1]/div/bf-main-market/bf-main-marketview/div/div[2]/bf-marketview-runners-list[2]/div/div/div/table/tbody/tr[3]/td[7]/button/div/span[2]'
    
        # get the data ++++++++++++++++++++++++++

        # team names
        
        h_tn = driver.find_element_by_xpath(h_tn_xp).text
        a_tn = driver.find_element_by_xpath(a_tn_xp).text
        d_tn = driver.find_element_by_xpath(d_tn_xp).text

        # home team - back
        h_b1_o = driver.find_element_by_xpath(h_b1_o_xp).text
        h_b1_c = driver.find_element_by_xpath(h_b1_c_xp).text
        h_b2_o = driver.find_element_by_xpath(h_b2_o_xp).text
        h_b2_c = driver.find_element_by_xpath(h_b2_c_xp).text
        h_b3_o = driver.find_element_by_xpath(h_b3_o_xp).text
        h_b3_c = driver.find_element_by_xpath(h_b3_c_xp).text
        # home team - lay
        h_l1_o = driver.find_element_by_xpath(h_l1_o_xp).text
        h_l1_c = driver.find_element_by_xpath(h_l1_c_xp).text
        h_l2_o = driver.find_element_by_xpath(h_l2_o_xp).text
        h_l2_c = driver.find_element_by_xpath(h_l2_c_xp).text
        h_l3_o = driver.find_element_by_xpath(h_l3_o_xp).text
        h_l3_c = driver.find_element_by_xpath(h_l3_c_xp).text
        
        # away team - back
        a_b1_o = driver.find_element_by_xpath(a_b1_o_xp).text
        a_b1_c = driver.find_element_by_xpath(a_b1_c_xp).text
        a_b2_o = driver.find_element_by_xpath(a_b2_o_xp).text
        a_b2_c = driver.find_element_by_xpath(a_b2_c_xp).text
        a_b3_o = driver.find_element_by_xpath(a_b3_o_xp).text
        a_b3_c = driver.find_element_by_xpath(a_b3_c_xp).text
        # away team - lay
        a_l1_o = driver.find_element_by_xpath(a_l1_o_xp).text
        a_l1_c = driver.find_element_by_xpath(a_l1_c_xp).text
        a_l2_o = driver.find_element_by_xpath(a_l2_o_xp).text
        a_l2_c = driver.find_element_by_xpath(a_l2_c_xp).text
        a_l3_o = driver.find_element_by_xpath(a_l3_o_xp).text
        a_l3_c = driver.find_element_by_xpath(a_l3_c_xp).text
    
        # draw - back
        d_b1_o = driver.find_element_by_xpath(d_b1_o_xp).text
        d_b1_c = driver.find_element_by_xpath(d_b1_c_xp).text
        d_b2_o = driver.find_element_by_xpath(d_b2_o_xp).text
        d_b2_c = driver.find_element_by_xpath(d_b2_c_xp).text
        d_b3_o = driver.find_element_by_xpath(d_b3_o_xp).text
        d_b3_c = driver.find_element_by_xpath(d_b3_c_xp).text
        # draw team - lay
        d_l1_o = driver.find_element_by_xpath(d_l1_o_xp).text
        d_l1_c = driver.find_element_by_xpath(d_l1_c_xp).text
        d_l2_o = driver.find_element_by_xpath(d_l2_o_xp).text
        d_l2_c = driver.find_element_by_xpath(d_l2_c_xp).text
        d_l3_o = driver.find_element_by_xpath(d_l3_o_xp).text
        d_l3_c = driver.find_element_by_xpath(d_l3_c_xp).text
        
        #tree_h.item('item1', text=(d_l3_o), values = d_l3_c)
        #tree_h.item('item1', text=(d_l1_c), values = 234)
        
        #time.sleep(3)

        tree_h.item('h_b1_t', text = h_b1_o, values = h_b1_c) # insert item 1
        tree_h.item('h_b2_t', text = h_b2_o, values = h_b2_c) # insert item 1
        tree_h.item('h_b3_t', text = h_b3_o, values = h_b3_c) # insert item 1
        tree_h.item('h_l1_t', text = h_l1_o, values = h_l1_c) # insert item 1
        tree_h.item('h_l2_t', text = h_l2_o, values = h_l2_c) # insert item 1
        tree_h.item('h_l3_t', text = h_l3_o, values = h_l3_c) # insert item 1

        tree_a.item('a_b1_t', text = a_b1_o, values = a_b1_c) # insert item 1
        tree_a.item('a_b2_t', text = a_b2_o, values = a_b2_c) # insert item 1
        tree_a.item('a_b3_t', text = a_b3_o, values = a_b3_c) # insert item 1
        tree_a.item('a_l1_t', text = a_l1_o, values = a_l1_c) # insert item 1
        tree_a.item('a_l2_t', text = a_l2_o, values = a_l2_c) # insert item 1
        tree_a.item('a_l3_t', text = a_l3_o, values = a_l3_c) # insert item 1

        tree_d.item('d_b1_t', text = d_b1_o, values = d_b1_c) # insert item 1
        tree_d.item('d_b2_t', text = d_b2_o, values = d_b2_c) # insert item 
        tree_d.item('d_b3_t', text = d_b3_o, values = d_b3_c) # insert item 1
        tree_d.item('d_l1_t', text = d_l1_o, values = d_l1_c) # insert item 1
        tree_d.item('d_l2_t', text = d_l2_o, values = d_l2_c) # insert item 1
        tree_d.item('d_l3_t', text = d_l3_o, values = d_l3_c) # insert item 1

        Label(bet_overview, text=h_tn).grid(row=3, column = 2)
        Label(bet_overview, text=a_tn).grid(row=3, column = 5)
        Label(bet_overview, text=d_tn).grid(row=3, column = 8)
        

        tree_h.update_idletasks()
        tree_a.update_idletasks()
        tree_d.update_idletasks()

        #print("w8")

    def record_football_data(self,driver):

        # Connect to database
        conn = sqlite3.connect('bet_data_4.db')

        # Create a cursor object and call it for SQL commands
        c = conn.cursor()

        # Create bet data table
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
            away_lay_volume real)""")
        except:
            pass
        
        # link:   https://www.betfair.com/exchange/plus/football
        # Parse through betfair table

        for league in range(1,6):
            for row in range(1,15):
                            
                bet_data = RecordedData(league,row)

                # Check against not available to trigger end of array
                if bet_data.home_team_name == "not available":
                    break
                # If Check #1 is passed then add data to array
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
                :away_lay_volume)""",{
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
                'away_lay_volume':bet_data.away_lay_volume})
                
                # Commit data to database
                conn.commit()
        
        conn.close()

    #====================== Enter market =====================

    def enter_market(self):
        tree_h.selection_clear()
        selected_items = tree_a.selection_clear  
        print("hello")


    def clear_selection(self):
        tree_h.selection_clear # clear selection
        tree_h.selection_remove(tree_h.focus()) # clear focus

        tree_a.selection_clear # clear selection
        tree_a.selection_remove(tree_a.focus()) # clear focus

        tree_d.selection_clear # clear selection
        tree_d.selection_remove(tree_d.focus()) # clear focus 


    #====================== Exit market =====================
    def exit_market(self):
        tree_a.selection_clear
        print("hello")
        pass



form = tk.Tk()


client = ThreadedClient(form)

form.mainloop()


