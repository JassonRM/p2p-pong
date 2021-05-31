import datetime
import json
from player_connection_info import PlayerInfo


class PlayerList():

    def __init__(self):
        self.playerList = []

    def filter_players(self):
        newList = [player for player in self.playerList if int(datetime.datetime.now().minute) - player.time > 5]
        self.playerList = newList

    def get_list_as_JSON(self):
        return json.dumps(self.__dict__)

    def set_list_from_Json(self, json_str):
        array = json.loads(json_str)
        self.playerList = []
        for player in array:
            newPlayer = PlayerInfo(player["ip"], player["port"], player["time"], player["name"])
            self.playerList.append(newPlayer)
        self.playerList.remove()
        return

    def add_or_change(self, player_info_str):
        player = json.loads(player_info_str)

        for info in self.playerList:
            if info.ip == player["ip"]:
                info.set_time(int(player["time"]))
        player_info = PlayerInfo(player["ip"], player["port"], player["time"], player["name"])
        self.playerList.append(player_info)

    def populate_with_get(self):
        pass

    def to_str_list(self):
        string_list = []
        for element in self.playerList:
            string_list.append(f"Player:{element.name} ")

    def remove(self, json_str):
        player = json.loads(json_str)
        for ingo in self.playerList:
            if ingo.ip == player["ip"] and ingo.port == player["port"]:
                self.playerList.remove(ingo)
                return
