###############################################################################
# FILE : for_in_a_row.py
# WRITER : Ori Becher, orib_222 ,Bar Schwartz, bar4411
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION: Execution of connect4 game.
###############################################################################

import numpy
import tkinter as tk
import socket
from communicator import Communicator
from ai import *
from game import *
import sys
from game import Game


SERVER_FRAME_TITLE = 'server'
CLIENT_FRAME_TITLE = 'client'
PLACE_OF_IP = 3
WRONG_PLAYER = "please insert player either ai or human"
if __name__ == '__main__':

    if sys.argv[1] == 'ai':
        is_ai = True
    elif sys.argv[1] == 'human':
        is_ai = False
    else:
        raise Exception(WRONG_PLAYER)
    port = 8000
    root = tk.Tk()
    game = Game()

    if len(sys.argv) == PLACE_OF_IP:
        platform = Gui(root, port, is_ai, game)
        root.title(SERVER_FRAME_TITLE)
    else:
        platform = Gui(root, port, is_ai, game, sys.argv[PLACE_OF_IP])
        root.title(CLIENT_FRAME_TITLE)
    root.mainloop()
