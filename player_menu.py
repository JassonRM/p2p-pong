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



    # def search(self):
    #     pass
    #
    # def host(self):
    #     for elements in self.get_widgets():
    #         self.remove_widget(elements)
    #     self.add.text_input("Port:",default="8080")
    #     self.inputPort = self.get_widgets()[0]
    #     self.add.text_input("Name:", default="Prof")
    #     self.inputName = self.get_widgets()[1]
    #     local_ip = socket.gethostbyname(socket.gethostname())
    #     self.player_info.ip = local_ip
    #     self.add.label(f"Your Ip: {local_ip}")
    #     self.add.button("look for players",self.wait_for_player)
    #
    #
    # def wait_for_player(self):
    #
    #     try:
    #         self.connection.port = int(self.inputPort.get_value())
    #         self.player_info.name = self.inputName.get_value()
    #         self.player_info.port = self.connection.port
    #         self.add.label("Waiting for players...")
    #
    #     except:
    #         for elements in self.get_widgets():
    #             self.remove_widget(elements)
    #         self.add.label("Error, port should be a number")
    #         self.host()
    #





