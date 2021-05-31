import datetime
import json


class PlayerInfo():
    def __init__(self, port="", ip="", time=0, name="No"):
        self.port = port
        self.ip = ip
        self.name = name
        if time == 0:
            self.time = int(datetime.datetime.now().minute)
        else:
            self.time = time

    def compare(self, playerInfo):
        if playerInfo.ip == self.ip:
            return True
        else:
            return False

    def set_time(self, time):
        self.time = time

    def to_string(self):
        json.dumps(self.__dict__)
