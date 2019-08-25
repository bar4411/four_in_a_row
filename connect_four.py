import numpy
import tkinter as tk
import socket
from communicator import Communicator
from ai import *
from game import *
import sys
from game import Game
PLACE_OF_IP = 3


if __name__ == '__main__':

    if sys.argv[1] == 'ai':
        is_ai = True
    else:
        is_ai = False
    port = 8000
    root = tk.Tk()
    game = Game()

    if len(sys.argv) == PLACE_OF_IP:
        platform = Gui(root, port, is_ai, game)
        root.title("Server")
    else:
        platform = Gui(root, port, is_ai, game, sys.argv[PLACE_OF_IP])
        root.title("Client")
    root.mainloop()

