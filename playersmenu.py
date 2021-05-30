import socket

import pygame_menu.events
from pygame_menu import Menu
import http_request
from tkinter import messagebox as mbox


class PlayersMenu(Menu):
    def __init__(self,len,width,name,theme = 0):
        self.inputPort = 0
        super().__init__(name,width,len,theme = theme)
        self.add.button("Host game",self.host)
        self.add.button("Search Game",self.search)
        self.iputName = 0

    def search(self):
        pass

    def host(self):
        for elements in self.get_widgets():
            self.remove_widget(elements)
        self.add.text_input("Port:",default="8080")
        self.inputPort = self.get_widgets()[0]
        self.add.text_input("Name:", default="Prof")
        local_ip = socket.gethostbyname(socket.gethostname())
        self.add.label(f"Your Ip: {local_ip}")




