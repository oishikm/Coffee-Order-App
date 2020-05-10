# App to receive coffee order
# Oishik M | 10 May 2020

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from datetime import datetime
from random import randint
from os import chdir, remove, mkdir, listdir

class CoffeeWidget(Widget):
    ctr = None
    orderFile = None
    t = None
    orderID = None
    timestamp = None
    
    def __init__(self):
        super().__init__()
        self.initOrder()

    def stampOrderHeader(self):
        self.orderFile.write(self.timestamp)
        self.orderFile.write(str("Order ID: " + self.orderID + "\n"))

    def initOrder(self):
        self.ctr = 1
        self.t = datetime.now()
        self.orderID = str(chr(randint(65, 90)) + str(randint(1,99)))
        self.timestamp = str(self.t.strftime("%c")) + '\n'
        self.orderFileName = "ORDER_" + self.orderID + ".txt"
        self.orderFile = open(self.orderFileName, "w+")
        self.stampOrderHeader()

    def restartOrder(self):
        self.ctr = 1
        self.stampOrderHeader()
    
    def submit(self, coffeeType):
        self.orderFile.write(str(str(self.ctr) + '. ' + coffeeType + '\n'))
        self.ctr += 1

    def clearOrder(self):
        self.orderFile.seek(0)
        self.orderFile.truncate()
        self.restartOrder()
    
    def finishOrder(self):
        self.orderFile.seek(0)
        order = self.orderFile.read()
        self.orderFile.close()
        
        if self.ctr == 1:
            popup = Popup(title='Order rejected :(', content=Label(text="No coffee ordered !"), size_hint=(None, None), size=(400, 400))
            popup.open()
            remove(self.orderFileName)
        else:
            popup = Popup(title='Order received ! :D', content=Label(text=order), size_hint=(None, None), size=(400, 400))
            popup.open()
        
        self.initOrder()

class CoffeeOrderApp(App):
    def build(self):
        return CoffeeWidget()

if __name__ == "__main__" :
    if 'Orders' not in listdir():
        mkdir('Orders')
    chdir('Orders')
    appInstance = CoffeeOrderApp()
    appInstance.run()