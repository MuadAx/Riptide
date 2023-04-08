import cloudscraper,secrets,os
from bs4 import BeautifulSoup as bu
from time import sleep
from threading import Thread
from uuid import uuid4
class Muad():
    def getit(self):
        response = self.scraper.get(f"https://usr.gg/market?keyword=&sort=instagram&type={self.lenth}&starting_price=&last_price=")
        if response.status_code == 200:
            soup = bu(response.text, 'html.parser')
            for link in soup.find_all('a'):
                    url= link.get('href')
                    if url.__contains__("/account/"):
                        if url not in self.Urls:
                                response2 = self.scraper.get(url)
                                if response2.status_code== 200:
                                    self.ok+=1
                                    user1 = response2.text.split("<h1>@")[1]
                                    user = user1.split("</h1>")[0]
                                    if user not in self.Users:
                                        self.Users.append(user)
                                        open("users.txt","a").write(user+"\n")
                                elif response2.status_code == 429:
                                     self.rate+=1
                                else:
                                    self.error+=1
        elif response.status_code== 429:
             self.rate+=1
        else:
             self.error+=1
    def counter(self):
         while 1:
              os.system(f"title Ok : [{self.ok}] - RL : [{self.rate}] - Error : [{self.error}]")
    def __init__(self):
        self.ok= 0
        self.rate = 0
        self.error = 0
        self.Users = []
        self.lenth = ""
        self.userslist = open("users.txt","a")
        self.scraper = cloudscraper.create_scraper()
        self.Urls = []
        mode =input("[1] 1L\n[2] 2L \n[3] 3L\n[4] 4L \n[5] All\n=>")
        if mode.__contains__("1"):
             self.lenth ="1"
        elif mode.__contains__("2"):
             self.lenth = "2"
        elif mode.__contains__("3"):
             self.lenth = "3"
        elif mode.__contains__("4"):
             self.lenth ="4"
        elif mode.__contains__("5"):
             self.lenth = "all"
        Thread(None,self.counter).start()
        while 1:
             self.getit()
Muad()