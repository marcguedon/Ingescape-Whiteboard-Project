#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Puissance4_Controller.py
#  Puissance4_Controller version 1.0
#  Created by Ingenuity i/o on 2024/11/07
#
# "no description"
#
import ingescape as igs
import keyboard
import threading


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Puissance4_Controller(metaclass=Singleton):
    def __init__(self):
        self.board = None
        self.players_color = None
        self.token_placed_event = threading.Event()

    # Services
    def Token_Placed(self, sender_agent_name, sender_agent_uuid):
        '''
        Callback service to notify that the token transition is done
        '''

        self.token_placed_event.set()

    def run_game(self):
        '''
        Main function to run the game
        Choose tokens color for each player and play one round
        '''

        self.choose_tokens_color()
        self.play_round()

    def play_round(self):
        '''
        Function to play one round of the game
        '''

        self.board = [[0 for i in range(7)] for j in range(6)]
        igs.service_call("Puissance4_View", "init_game", (), "")
        player = 1

        while True:
            igs.service_call("Puissance4_View", "show_playing_player", (player), "")

            row, column = self.select_case(player)
            self.board[row][column] = player

            igs.service_call("Puissance4_View", "place_token", (player, row, column), "")
            self.token_placed_event.clear()
            self.token_placed_event.wait()

            winning_segment = self.check_winner(player)
            if winning_segment is not None:
                igs.service_call("Puissance4_View", "show_winner", (player, winning_segment[0][0], winning_segment[0][1], winning_segment[1][0], winning_segment[1][1]), "")
                break

            if self.is_board_full():
                igs.service_call("Puissance4_View", "show_winner", (-1, 0, 0, 0, 0), "")
                break

            player = 2 if player == 1 else 1

        keyboard.wait("enter")

    def get_row_from_column(self, player:int, column:int) -> int:
        '''
        Function to get the row where the token will be placed in the given column
        Input:
            player: int (the current player)
            column: int (the column where the token will be placed)
        Output:
            row: int (the row where the token will be placed. row = -1 if the column is full)
        '''

        for row in range(0, 6, 1):
            if self.board[row][column] == 0:
                return row
            
        return -1    
    
    def select_case(self, player:int) -> tuple[int, int]:
        '''
        Function to select the case where the token will be placed
        Input:
            player: int (the current player)
        Output:
            row, column: tuple[int, int] (the row and the column where the token will be placed)
        '''

        column = 0
        while self.get_row_from_column(player, column) == -1:
            column = (column + 1) % 7

        igs.service_call("Puissance4_View", "preview_token", (column, self.players_color[player-1]), "token")

        def find_next_column(column:int, direction:int) -> int:
            '''
            Function to find the next column where the token can be placed
            Inputs:
                column: int (the current column)
                direction: int (the direction to search the next column)
            Output:
                next_free_column: int (the next column where the token can be placed)
            '''

            next_free_column = column

            for _ in range(7):
                next_free_column = (next_free_column + direction) % 7

                if self.get_row_from_column(player, next_free_column) != -1:
                    return next_free_column
                
            return column

        def on_left_press():
            '''
            Function to handle the left key press event
            '''

            nonlocal column
            column = find_next_column(column, -1)
            igs.service_call("Puissance4_View", "preview_token", (column, self.players_color[player-1]), "token")

        def on_right_press():
            '''
            Function to handle the right key press event
            '''

            nonlocal column
            column = find_next_column(column, 1)
            igs.service_call("Puissance4_View", "preview_token", (column, self.players_color[player-1]), "token")

        keyboard.on_press_key("left", lambda _: on_left_press())
        keyboard.on_press_key("right", lambda _: on_right_press())
        keyboard.wait("down")
        keyboard.unhook_all()

        row = self.get_row_from_column(player, column)
        
        return (row, column)

    def is_board_full(self) -> bool:
        '''
        Function to check if the board is full
        Output:
            bool (True if the board is full, False otherwise)
        '''

        for row in range(6):
            for col in range(7):
                if self.board[row][col] == 0:
                    return False
        return True

    def check_winner(self, player:int) -> tuple[tuple[int, int], tuple[int, int]]:
        '''
        Function to check if the player has won the game
        Input:
            player: int (the current player)
        Output:
            winning_segment: tuple[tuple[int, int], tuple[int, int]] (the two points/endings of the winning segment. Return None if no winner)
        '''

        rows = len(self.board)
        cols = len(self.board[0])
        
        # Horizontal check
        for row in range(rows):
            for col in range(cols - 3):
                if (self.board[row][col] == player and
                    self.board[row][col + 1] == player and
                    self.board[row][col + 2] == player and
                    self.board[row][col + 3] == player):
                    return ((row, col), (row, col + 3))

        # Vertical check
        for row in range(rows - 3):
            for col in range(cols):
                if (self.board[row][col] == player and
                    self.board[row + 1][col] == player and
                    self.board[row + 2][col] == player and
                    self.board[row + 3][col] == player):
                    return ((row, col), (row + 3, col))

        # Diagonal check (top-left to bottom-right)
        for row in range(rows - 3):
            for col in range(cols - 3):
                if (self.board[row][col] == player and
                    self.board[row + 1][col + 1] == player and
                    self.board[row + 2][col + 2] == player and
                    self.board[row + 3][col + 3] == player):
                    return ((row, col), (row + 3, col + 3))

        # Diagonal check (top-right to bottom-left)
        for row in range(rows - 3):
            for col in range(3, cols):
                if (self.board[row][col] == player and
                    self.board[row + 1][col - 1] == player and
                    self.board[row + 2][col - 2] == player and
                    self.board[row + 3][col - 3] == player):
                    return ((row, col), (row + 3, col - 3))

        return None

    def choose_tokens_color(self):
        '''
        Function to choose tokens color for each player
        '''

        igs.service_call("Puissance4_View", "init_color_choice", (), "")

        self.players_color = ["", ""]
        color_list = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "brown", "grey"]

        for player in range(1, 3):
            igs.service_call("Puissance4_View", "show_choosing_player", (player), "")

            color_list = [color for color in color_list if color not in self.players_color]
            index = 0
            igs.service_call("Puissance4_View", "choose_token_color", (color_list[index]), "")

            def on_left_press():
                '''
                Function to handle the left key press event
                '''

                nonlocal index
                index = (index - 1) % len(color_list)
                igs.service_call("Puissance4_View", "choose_token_color", (color_list[index]), "")

            def on_right_press():
                '''
                Function to handle the right key press event
                '''

                nonlocal index
                index = (index + 1) % len(color_list)
                igs.service_call("Puissance4_View", "choose_token_color", (color_list[index]), "")

            keyboard.on_press_key("left", lambda _: on_left_press())
            keyboard.on_press_key("right", lambda _: on_right_press())
            keyboard.wait("enter")

            self.players_color[player-1] = color_list[index]

            keyboard.unhook_all()