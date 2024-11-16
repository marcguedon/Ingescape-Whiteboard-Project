#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Puissance4_View.py
#  Puissance4_View version 1.0
#  Created by Ingenuity i/o on 2024/11/07
#
# "no description"
#
import ingescape as igs
from pathlib import Path


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Puissance4_View(metaclass=Singleton):
    def __init__(self):
        self.elements_list = {}
        base_path = Path(__file__).resolve().parent.parent
        self.data_path = base_path / "data"

        # outputs
        self._Game_TitleO = None

    # outputs
    @property
    def Game_TitleO(self):
        return self._Game_TitleO

    @Game_TitleO.setter
    def Game_TitleO(self, value:str):
        self._Game_TitleO = value
        if self._Game_TitleO is not None:
            igs.output_set_string("game_title", self._Game_TitleO)

    # Services
    def Elementcreated(self, sender_agent_name, sender_agent_uuid, elementId, token):
        '''
        Callback service to handle the creation of an element
        Inputs:
            elementId: int (representing the element ID)
            token: str (representing the token)
        '''

        self.elements_list[token] = elementId

    def Actionresult(self, sender_agent_name, sender_agent_uuid, token):
        '''
        Callback service to handle the action result of the "translate" service
        Input:
            token: str (representing the token)
        '''

        if token == "last_translate":
            igs.service_call("Puissance4_Controller", "token_placed", (), "")
            
    def Show_Choosing_Player(self, sender_agent_name, sender_agent_uuid, Player):
        '''
        Service to show the player who is choosing his color
        Input:
            Player: int (representing the current player)
        '''

        igs.service_call("Whiteboard", "chat", ("Joueur " + str(Player) + ", choisissez votre couleur."), "")

        if "player" in self.elements_list:
            igs.service_call("Whiteboard", "remove", (self.elements_list["player"]), "")

        image_path = self.data_path / f"p{Player}.png"
        igs.service_call("Whiteboard", "addImageFromUrl", (f"file:///{image_path}", 75.0, 105.0), "player")
        
    def Choose_Token_Color(self, sender_agent_name, sender_agent_uuid, Color):
        '''
        Service to choose the color of the token/player
        Input:
            Color: str (representing the color of the token/player)
        '''

        if "color" in self.elements_list:
            igs.service_call("Whiteboard", "setStringProperty", (self.elements_list["color"], "fill", Color), "")
        
        else:
            igs.service_call("Whiteboard", "addShape", ("ellipse", 450.0, 80.0, 300.0, 300.0, Color, 0.0, 0.0), "color")

    def Preview_Token(self, sender_agent_name, sender_agent_uuid, Column_Number, Color):
        '''
        Service to preview a token on the grid
        Inputs:
            Column_Number: int (representing the column number where the token is previewed)
            Color: str (representing the color of the token/player)
        '''

        if "token" not in self.elements_list:
            igs.service_call("Whiteboard", "addShape", ("ellipse", (Column_Number+1) * 100.0 + 167.0, 5.0, 70.0, 70.0, Color, 0.0, 0.0), "token")

        else:
            igs.service_call("Whiteboard", "moveTo", (self.elements_list["token"], (Column_Number+1) * 100.0 + 167.0, 5.0), "")
        
    def Place_Token(self, sender_agent_name, sender_agent_uuid, Player, Line_Number, Column_Number):
        '''
        Service to place (translate) a token on the grid
        Inputs:
            Player: int (representing the player)
            Line_Number: int (representing the line number where the token is placed)
            Column_Number: int (representing the column number where the token is placed)
        '''

        igs.service_call("Whiteboard", "chat", ("Joueur " + str(Player) + " a placé un jeton en " + str(Column_Number+1) + "."), "")

        for _ in range(0, 561 - Line_Number * 100, 1):
            igs.service_call("Whiteboard", "translate", (self.elements_list["token"], 0.0, 1.0), "")

        igs.service_call("Whiteboard", "translate", (self.elements_list["token"], 0.0, 1.0), "last_translate")
        self.elements_list.pop("token", None)

    def Show_Playing_Player(self, sender_agent_name, sender_agent_uuid, Player):
        '''
        Service to show the playing player
        Input:
            Player: int (representing the playing player)
        '''

        igs.service_call("Whiteboard", "chat", ("Au tour de joueur " + str(Player) + " !"), "")

        if "player" in self.elements_list:
            igs.service_call("Whiteboard", "remove", (self.elements_list["player"]), "")

        image_path = self.data_path / f"p{Player}.png"
        igs.service_call("Whiteboard", "addImageFromUrl", (f"file:///{image_path}", 75.0, 105.0), "player")
        
    def Show_Winner(self, sender_agent_name, sender_agent_uuid, Player, Winning_Segment):
        '''
        Service to show the winner of the game
        Inputs:
            Player: int (representing the winning player, Player = -1 if it's a draw)
            Winning_Segment: tuple of two tuples of integers (corresponding to the coordinates of the tow points/extremities of the winning segment)
        '''

        igs.service_call("Whiteboard", "remove", (0), "")

        if (Player == -1):
            igs.service_call("Whiteboard", "chat", ("Match nul !"), "")
            igs.service_call("Whiteboard", "addText", ("Match nul !", 510.0, 660.0, "black"), "")
        
        else:
            self.show_winning_segment(Winning_Segment)

            igs.service_call("Whiteboard", "chat", ("Joueur " + str(Player) + " a gagné la manche !"), "")
            igs.service_call("Whiteboard", "addText", ("Joueur " + str(Player) + " a gagné la manche ! (Entrer pour rejouer)", 205.0, 660.0, "black"), "")

        igs.service_call("Whiteboard", "chat", ("Pressez Entrer pour commencer une nouvelle manche."), "")

    def Init_Color_Choice(self, sender_agent_name, sender_agent_uuid):
        '''
        Service to initialize the color choice
        '''

        self.elements_list = {}

        igs.service_call("Whiteboard", "hideLabels", (), "")
        igs.service_call("Whiteboard", "clear", (), "")

        igs.service_call("Whiteboard", "chat", ("Nouvelle manche."), "")
        igs.service_call("Whiteboard", "chat", ("← ou → pour changer de couleur, \"enter\" pour accepter."), "")
        igs.service_call("Whiteboard", "addText", ("Choisissez votre couleur.", 400.0, 420.0, "black"), "")
        igs.service_call("Whiteboard", "addText", ("← ou → pour changer de couleur, \"enter\" pour accepter", 170.0, 660.0, "black"), "")

    def Init_Game(self, sender_agent_name, sender_agent_uuid):
        '''
        Service to initialize the game
        '''

        igs.service_call("Whiteboard", "clear", (), "")
        self.elements_list.pop("player", None)

        igs.service_call("Whiteboard", "chat", ("← ou → pour changer de colonne, ↓ pour placer le jeton."), "")
        igs.service_call("Whiteboard", "addText", ("← ou → pour changer de colonne, ↓ pour placer le jeton", 165.0, 660.0, "black"), "")

        # Draw the grid
        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 50.0, 700.0, 5.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 650.0, 705.0, 5.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 50.0, 5.0, 600.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 950.0, 50.0, 5.0, 605.0, "black", 0.0, 0.0), "")

        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 150.0, 700.0, 5.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 250.0, 700.0, 5.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 350.0, 700.0, 5.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 450.0, 700.0, 5.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 250.0, 550.0, 700.0, 5.0, "black", 0.0, 0.0), "")

        igs.service_call("Whiteboard", "addShape", ("rectangle", 350.0, 50.0, 5.0, 600.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 450.0, 50.0, 5.0, 600.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 550.0, 50.0, 5.0, 600.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 650.0, 50.0, 5.0, 600.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 750.0, 50.0, 5.0, 600.0, "black", 0.0, 0.0), "")
        igs.service_call("Whiteboard", "addShape", ("rectangle", 850.0, 50.0, 5.0, 600.0, "black", 0.0, 0.0), "")

    def show_winning_segment(self, winning_segment:tuple[tuple[int, int], tuple[int, int]]):
        '''
        Function to show the winning segment on the whiteboard
        Input:
            winning_segment: tuple of two tuples of integers (corresponding to the coordinates of the tow points/extremities of the winning segment)
        '''

        point1_row = 597 - winning_segment[0][0] * 100
        point1_col = (winning_segment[0][1] + 1) * 100.0 + 197.0
        point2_row = 597 - winning_segment[1][0] * 100
        point2_col = (winning_segment[1][1] + 1) * 100.0 + 197.0
        nb_points = 100
        
        for i in range(nb_points + 1):
            x = point1_col + (point2_col - point1_col) * i / nb_points
            y = point1_row + (point2_row - point1_row) * i / nb_points

            igs.service_call("Whiteboard", "addShape", ("ellipse", x, y, 10.0, 10.0, "black", 0.0, 0.0), "")