
#Beautiful soup url: https://www.crummy.com/software/BeautifulSoup/bs4/doc
# data input possibility: https://www.whoscored.com/Matches/1364326/Live/England-FA-Cup-2018-2019-Swansea-Manchester-City

import bs4
import matplotlib
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

Homearray=[]
HomePossessionarray=[]
Drawarray=[]
Awayarray=[]
AwayPossessionarray=[]
Timearray=[]

my_Beturl = 'https://www.betfair.com/exchange/plus/football'
my_Staturl = 'https://www.betfair.com/exchange/plus/football'

k=0
timestampini=time.time()
#style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

timestamp=0

while timestamp<300:
    
    def animate(i):

        #Opening a connection and grabbing the page
        #Betpage_html=uReq(my_Beturl).read()

        #Opening a connection and grabbing the page
        #Statpage_html=uReq(my_Staturl).read()
        
        #html parsing
        Betpage_html=uReq(my_Beturl).read() # read Bet page data
        Betpage_soup=soup(Betpage_html,"html.parser") # create Bet page soup
        Statpage_html=uReq(my_Staturl).read() # read stat page data
        Statpage_soup=soup(Statpage_html,"html.parser") # create stat page soup
    
        Betcontainers=Betpage_soup.findAll("table",{"class":"coupon-table"})
        Statcontainers=Statpage_soup.findAll("div",{"class":"toggle_content","id":"stats"})

        for container in Betcontainers: #Bet website analysis
            print(container)
            test = container.div.div.text.strip()
            if test != "Es stehen keine Märkte zur Verfügung":
                Hometeam = container.div.div.div.find("div",{"class":"minimarketview-content"}).ul.find("li",{"class":"runner-item"}).span
                Hometeamodds = container.div.div.div.find("div",{"class":"minimarketview-content"}).ul.find("li",{"class":"runner-item"}).a.span
            
                if Hometeamodds.text.strip() != "":
                    HometeamoddsF=float(Hometeamodds.text.strip())
                    Homearray.append(HometeamoddsF)
                else:
                    Homearray.append("0")

                Draw=Hometeam.find_next("li")
                Drawodds=Draw.a.span
                Drawarray.append(float(Drawodds.text.strip()))

                Awayteam = Draw.find_next("li").span
                Awayteamodds = Draw.find_next("li").a.span

                if Awayteamodds.text.strip() != "":
                    AwayteamoddsF=float(Awayteamodds.text.strip())
                    Awayarray.append(AwayteamoddsF)
                else:
                    Awayarray.append("0")

                timestamp=time.time()-timestampini
                Timearray.append(timestamp)
                
                

        for container in Statcontainers: #Stat website analysis
            #print(container)
            if test != "Es stehen keine Märkte zur Verfügung":
                HometeamPos=container.find("div",{"id":"stat_1"}).find("span",{"class":"m_home_stat"}).text.strip()
                HometeamPosF=float(HometeamPos.replace("%",""))
                HomePossessionarray.append(HometeamPosF)

                AwayteamPos=container.find("div",{"id":"stat_1"}).find("span",{"class":"m_away_stat"}).text.strip()
                AwayteamPosF=float(AwayteamPos.replace("%",""))
                AwayPossessionarray.append(AwayteamPosF)
            
                
        #print(Awayteamodds)
        #print(Hometeamodds)
        #print(timestamp)
        ax1.clear()
        ax1.plot(Timearray, Homearray,label=Hometeam.text.strip() + " - " + Hometeamodds.text.strip())
        ax1.plot(Timearray,Awayarray,label=Awayteam.text.strip() + " - " + Awayteamodds.text.strip())
        ax1.plot(Timearray,Drawarray, label="Draw")
        #ax1.plot(Timearray,HomePossessionarray, label = Hometeam.text.strip()+" Possession[%]")
        #ax1.plot(Timearray,AwayPossessionarray, label = Awayteam.text.strip()+" Possession[%]")
        plt.ylabel('Integer')
        plt.xlabel('Time [s]')
        plt.legend(loc='upper left')
        

    ani = animation.FuncAnimation(fig, animate, interval = 100)
    plt.show()



def my_plotter(ax1,data1,data2,data3, param_dict):
        """
        A helper function to make a graph

        Parameters
        ----------
        ax : Axes
            The axes to draw to

        data1 : Time data
        data2 : Hometeam title
        data3 : Hometeam odds
    
        param_dict : dict
           Dictionary of kwargs to pass to ax.plot

        Returns
        -------
        out : list
            list of artists added
        """
        data2=data2.text.strip()

        out = ax1.plot(data1, data3, label=data2,**param_dict)
        out = ax1.set_title('Odds vs Time')
        out = ax1.set_ylabel('Odds (dec)')
        out = ax1.set_xlabel('Time (s)')
        out = plt.legend()
        return out

def my_plotterP(ax2,data1,data2,data3, param_dict):
        """
        A helper function to make a graph

        Parameters
        ----------
        ax : Axes
            The axes to draw to

        data1 : Time data
        data2 : Hometeam title
        data3 : Hometeam odds
    
        param_dict : dict
           Dictionary of kwargs to pass to ax.plot

        Returns
        -------
        out : list
            list of artists added
        """
        data2=data2.text.strip() + " posession [%]"

        out = ax2.plot(data1, data3, label=data2,**param_dict)
        out = ax2.set_title('Possession vs Time')
        out = ax2.set_ylabel('Possession')
        out = ax2.set_xlabel('Time (s)')
        out = plt.legend()
        return out

# which you would then use as:

#data1, data2, data3, data4 = np.random.randn(4, 100)
#if test != "Es stehen keine Märkte zur Verfügung":
    #fig, (ax1, ax2) = plt.subplots(1, 2)
    #my_plotter(ax1, Timearray, Hometeam, Homearray,{'marker': ','})
    #my_plotter(ax1, Timearray, Awayteam, Awayarray,{'marker':','})
    #my_plotterP(ax2, Timearray, Hometeam, HomePossessionarray,{'marker':','})
    #my_plotterP(ax2, Timearray, Awayteam, AwayPossessionarray,{'marker':','})
    #plt.show()
#else: 
#print("Error - Bet data unavailable")