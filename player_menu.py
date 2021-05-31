import socket
from time import sleep

import pygame_menu.events
from pygame_menu import Menu
from tkinter import messagebox as mbox
from player_connection_info import PlayerInfo

class PlayersMenu(Menu):
    def __init__(self,len,width,name,connection,theme = 0):
        super().__init__(name,width,len,theme = theme)
        self.inputPort = 0
        self.player_info = PlayerInfo()
        self.connection = connection
        self.add.button("start",self.init_connection)
        self.add.button("close",pygame_menu.events.EXIT)

    def init_connection(self):
        for elements in self.get_widgets():
            self.remove_widget(elements)
        self.add.label("Searching players.....")
        self.connection.hole_punching()
        for elements in self.get_widgets():
            self.remove_widget(elements)
        self.add.label("Found a player")
        sleep(1)
        self.close()
