import requests
from bs4 import BeautifulSoup
import os
import discord

def cms(str:str)->str:
    page = requests.get("https://www.cardmarket.com/en/Magic/Products/Search?searchString=%s" %str)
    soup = BeautifulSoup(page.content, 'html.parser')
    elem = soup.find('div',class_='row no-gutters')
    a = elem.findAll("a")[1]
    link = a.get("href")
    name = a.get_text()
    price = elem.find("div",class_= "col-price").get_text()
    return ""+name+" [ "+price+" ]\n"+"https://www.cardmarket.com"+link 

def get_cards_list(st:str)->list:
    card_list = []
    condition = True
    while len(st)>0:
        print(st)
        start = st.find("[[")
        end = st.find("]]")
        #print("start = %d  end = %d"%(start,end))
        if(start!=-1 and end!=-1):
            start += 2
            #print("msg = %s"%st[start:end])
            card_list.append( st[start:end] )
            st = st[end+2:]
            
        else:
            break
    return card_list
    
def scan_and_answer(msg:str):
    cards_list = get_cards_list(msg)
    for card in cards_list:
        print(cms(card))

#msg = "@FulminRay  che succede se ho queste due creature in campo quando schianta una creatura avversaria? [[Kalitas, traitor of ghet]] [[Gisa, Glorious resurrector]]"
#scan_and_answer(msg)
#msg = input("card name: ")
#print(cms(msg)) [[Kalitas, traitor of ghet]] [[Gisa, Glorious resurrector]]



class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self,message):
        if message.author == client.user:
            return
        cards_list = get_cards_list(message.content)
        for card in cards_list:
            await message.channel.send(cms(card))

TOKEN = ''
client = MyClient()


client.run(TOKEN)
