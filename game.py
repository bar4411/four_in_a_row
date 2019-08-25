###############################################################################
# FILE : game.py
# WRITER : Ori Becher, orib_222 ,Bar Schwartz, bar4411
# EXERCISE : intro2cs ex9 2017-2018
# DESCRIPTION: contains class Game and Gui.
###############################################################################
import numpy
import tkinter as tk
import socket
from communicator import Communicator
from ai import AI
import sys


class Gui():
	"""
	class of the Gui wrapping the game
	"""

	SUM_OF_ALL_BOARD_CELLS = 7 * 6
	RANGE_BALL_CLICK = 60
	END_BARRIER_AXIS_X = 435
	START_BARRIER_BALLS_AXIS_X = 15
	END_OF_AXIS_Y_BALLS = 440
	START_SPACE_AXIS_Y = 90
	START_SPACE_AXIS_X = 20
	SPLITTER_OF_BALLS_AXIS_Y = 60
	SPLITTER_OF_BALLS_AXIS_X = 60
	NUM_OR_ROWS = 6
	NUM_OF_COLUNM = 7
	CANVAS_SIZE = 450
	BALL_SIZE = 50
	STEP_SIZE = 2
	WINNER_FONT = ("Helvetica", 20)
	WINNER_MSG = "The winner is the"
	BACKGROUND_COL = "#6495ED"
	DEFAULT_DISC_COL = 'white'
	PLAYER1_COL = "red"
	WIN_COL = 'yellow'
	PLAYER2_COL = "#008000"
	NO_WIN_MSG = "no one wins"
	WIN_MSG = "You win"
	LOOSE_MSG = 'You loose'
	BEST_AI_DEFAULT = 0
	YOUR_TURN_LABEL='For playing your turn\nclick on the wanted column'
	LABEL_COLOR='white'
	LABEL_X_PLACE=65
	LABEL_Y_PLACE=15

	def __init__(self, parent, port, is_ai, game, ip=None):
		"""
		constructor of Gui
		:param parent: root of the platform
		:param port: to conect
		:param is_ai: True if this player is the computer
		:param ip: of the server.
		"""
		#
		self.game = game

		self.best_ai_move = self.BEST_AI_DEFAULT

		self.ip = ip

		# server begins the game
		if not ip:
			self.__my_turn = True

		else:
			self.__my_turn = False

		# initial interface
		self._parent = parent
		self._canvas = tk.Canvas(parent, width=self.CANVAS_SIZE,
								 height=self.CANVAS_SIZE, bg=self.BACKGROUND_COL)
		self._disc_places = []
		self._prepeare_canvas()

		if is_ai:
			self.is_ai = True
			self.ai = AI()
		else:
			self.is_ai = False
			self._canvas.bind("<Button-1>", self.click_bind)
		self._canvas.pack()

		# communication:
		self.__communicator = Communicator(parent, port, ip)
		self.__communicator.connect()
		self.__communicator.bind_action_to_message(self.__handle_message)

		# if self is server and ai then responds immediately
		if is_ai and not ip:
			self.modify_my_turn(True)
			self.respond()

		if not is_ai:

			self.__put_labal()


	def __put_labal(self):


		self.__label=tk.Label(self._parent,text=self.YOUR_TURN_LABEL,
							  fg=self.LABEL_COLOR,font=("Garamond", 20, "bold"),bg=self.BACKGROUND_COL)
		self.__label.pack()
		self.__label.place(x=self.LABEL_X_PLACE, y=self.LABEL_Y_PLACE)


	def __handle_message(self, col=None):
		"""
		sends the massage of the player from the other side to the board
		:param col: number of column
		:return: None
		"""

		self.game.make_move(int(col))
		self._update_interface()
		if self.game.get_winner()[0] != self.game.NO_WINNER:
			self.declare_winner()
			return
		self.modify_my_turn(True)

		if self.is_ai:
			self.respond()

	def click_bind(self, event):
		"""
		for every click of the left button of the mouse the func
		interperts it to the column that the player wanted
		:param event: the coordinates of the click on the canvas
		:return: transfer the column to the func  board.make_move()
		"""
		if self.is_my_turn():
			self.game.set_turn(True)
			if self.START_SPACE_AXIS_Y <= event.y <= self.END_OF_AXIS_Y_BALLS and \
					self.START_BARRIER_BALLS_AXIS_X <= event.x <= self.END_BARRIER_AXIS_X:
				col = (event.x - self.START_BARRIER_BALLS_AXIS_X) // self.RANGE_BALL_CLICK
				self.respond(col)

	def respond(self, col=None):
		"""make the next current player move"""
		if not self.is_ai:
			try:
				column = self.game.make_move(col)
				self.send_to_other_player(col)
				self._update_interface()
				winner = self.game.get_winner()[0]
				if winner != self.game.NO_WINNER and not self.is_ai:
					self._canvas.unbind("<Button-1>")
					self.declare_winner()
				self.modify_my_turn(False)
			except:
				return None
		else:
			col = self.ai.find_legal_move(self.game, self.ai_func)
			self._update_interface()
			if self.game.get_winner()[0] != self.game.NO_WINNER:
				self.declare_winner()
			self.send_to_other_player(col)
			self.modify_my_turn(False)

	def ai_func(self, column):
		"""The next function is not necessary to the course team
		It's the function which records every potential ai moves
		 it the ai will finish all moves it will put -1 in the
		function and the ouput will be the last ai move"""

		if column not in range(len(self.game.board[0])):
			return self.game.make_move(self.best_ai_move)
		else:
			self.best_ai_move = column

	def _update_interface(self):
		"""updates Gui interface so it will fit the acutal board"""
		for col in range(len(self.game.board[0])):
			for row in range(len(self.game.board)):
				if self.game.board[row][col] == self.game.PLAYER_ONE:
					self.paint_the_disc(col, row, self.game.PLAYER_ONE)
				elif self.game.board[row][col] == self.game.PLAYER_TWO:
					self.paint_the_disc(col, row, self.game.PLAYER_TWO)

	def _prepeare_canvas(self):
		"""
		paints on the canvas ovals(discs)
		:return: None
		"""
		balls = []
		for col_x in range(self.NUM_OF_COLUNM):
			for row_y in range(self.NUM_OR_ROWS):
				x = self.START_SPACE_AXIS_X + self.SPLITTER_OF_BALLS_AXIS_X * col_x
				y = self.START_SPACE_AXIS_Y + self.SPLITTER_OF_BALLS_AXIS_Y * row_y
				self._canvas.create_oval(x, y, x + self.BALL_SIZE,
										 y + self.BALL_SIZE, fill=self.DEFAULT_DISC_COL)
				balls.append((x, y))
			self._disc_places.append(balls)
			balls = []

	def paint_the_disc(self, col_x, row_y, player, color=None):
		"""
		the func gets the place of the disc that suppose to be paint,
		by the color of the player
		:param col_x:
		:param row_y:
		:return:
		"""
		x = self.START_SPACE_AXIS_X + self.SPLITTER_OF_BALLS_AXIS_X * col_x
		y = self.START_SPACE_AXIS_Y + self.SPLITTER_OF_BALLS_AXIS_Y * row_y
		if not color:
			if player == self.game.PLAYER_ONE:
				color = self.PLAYER1_COL
			else:
				color = self.PLAYER2_COL
		self._canvas.create_oval(x, y, x + self.BALL_SIZE,
								 y + self.BALL_SIZE, fill=color)

	def declare_winner(self):
		"""when a player wins it adds title
		Who is the winner"""

		winner_player = self.game.get_winner()
		if winner_player[0] == self.game.PLAYER_ONE:
			winner = self.WIN_MSG
		elif winner_player[0] == self.game.PLAYER_TWO:
			winner = self.LOOSE_MSG
		else:
			winner = self.NO_WIN_MSG
		if winner_player[0] != self.game.DRAW:

			for ball in winner_player[1]:
				self.paint_the_disc(ball[1], ball[0],
									winner_player[0], color=self.WIN_COL)
		label = tk.Label(self._parent, text=winner, font=self.WINNER_FONT)
		label.pack(side=tk.TOP)

	def send_to_other_player(self, column):
		"""
		sends to the other player the column that I clicked
		:param column:
		:return:
		"""
		if self.__my_turn:
			self.__communicator.send_message(column)

	def modify_my_turn(self, is_my_turn):
		"""
		boolenic changer if it's my turn or not.
		:param is_my_turn: True or False
		:return:
		"""

		self.__my_turn = is_my_turn
		self.game.set_turn(is_my_turn)

	def is_my_turn(self):
		"""
		:return: Ture or False if it's my turn
		"""
		return self.__my_turn


class Game:
	"""
	class of the game
	"""
	PLAYER_ONE = 0
	PLAYER_TWO = 1
	DRAW = 2
	NO_WINNER = 3
	PLACE_HOLDER = '-'
	COLS = 7
	ROWS = 6
	SUM_OF_ALL_BOARD_CELLS = COLS * ROWS
	WINING_SEQ = 4
	ILLEGAL_MOVE_MSG = 'Illegal move'

	def __init__(self):
		"""
		constructor of the game
		"""
		self.board = [[self.PLACE_HOLDER for i in range(self.COLS)] for j in range(self.ROWS)]
		self.__turn = None

	def make_move(self, column):
		"""
		the func put a disc of the player in
		the column was imputed. the disc will input firs to the maximum row that available.
		(we'll check first row 5 and then row 4 and so on...)
		:param column: integer of the column
		:return: True if column was legal and exception if there
		was illegal move.
		"""
		if column > len(self.board[0]):
			raise Exception(self.ILLEGAL_MOVE_MSG)
		index = len(self.board) - 1
		while index >= 0:
			if self.board[index][column] == self.PLACE_HOLDER:
				self.board[index][column] = self.get_current_player()
				# we fill the oval in the canvas with the player's color.
				return column
			index -= 1
		raise Exception(self.ILLEGAL_MOVE_MSG)

	def remove_move(self, column):
		"""removes the last move"""
		if column > len(self.board[0]):
			raise Exception(self.ILLEGAL_MOVE_MSG)
		index = 0
		while index < len(self.board):
			if self.board[index][column] != self.PLACE_HOLDER:
				self.board[index][column] = self.PLACE_HOLDER

				return column
			index += 1
		raise Exception(self.ILLEGAL_MOVE_MSG)

	def get_winner(self):
		"""
		the func is return the player if he's the winner and
		None if there is no winner.
		:return:
		"""
		counter_cells = 0
		dict_details = {'row': [0, 1], 'col': [1, 0], 'diagonal-A:': [1, 1], 'diagonal-B': [1, -1]}
		for row in range(len(self.board)):
			for col in range(len(self.board[0])):
				if self.get_player_at(row, col) == self.get_current_player():
					counter_cells += 1
					situation = self.__check_the_situation(self.get_player_at(row, col)
														   , row, col, dict_details)
					if situation[0]:
						return self.get_current_player(), situation[1]
		if counter_cells == self.SUM_OF_ALL_BOARD_CELLS:
			return self.DRAW,
		return self.NO_WINNER,

	def __check_the_situation(self, player, row, col, dict_details):
		"""
		the func do loop of all possible path to check winning
		and sent to an recursive aid func for check the winning.
		:param player: player 1 or 2 to check.
		:param row:
		:param col:
		:param dict_details: dict of paths and their movements.
		:return: True or False if winning was detected.
		"""
		path = [(row, col)]
		for position, moves in dict_details.items():
			try:
				if player == self.get_player_at(row + moves[0], col + moves[1]):
					new_row = row + moves[0]
					new_col = col + moves[1]
					output = self.__check_moves(player,
												new_row,
												new_col, moves, 1, path + [(new_row, new_col)])

					if output[0]:
						return output
			except IndexError:
				continue
		return False,

	def __check_moves(self, player, row, col, moves, index, path):
		"""
		recursive func to check winning while moving forward
		in the board.
		:param player: 1 or 2.
		:param row:
		:param col:
		:param moves: the possible moves in the specific path.
		:param index: counts the number of paths while 3 is the maximum where we'll return True.
		:return: True or False if there is a winning situation.
		:return
		"""

		try:
			if index == self.WINING_SEQ - 1:
				return True, path
			new_row = row + moves[0]
			new_col = col + moves[1]
			if self.get_player_at(new_row, new_col) == player:
				return self.__check_moves(player,
										  new_row, new_col,
										  moves, index + 1, path + [(new_row, new_col)])
			else:
				return False,
		except IndexError:
			return False,

	def get_player_at(self, row, col):
		"""
		the func check which player's disc is in the cell
		:param row:
		:param col:
		:return: 1 or 2 for the player or None if the cell empty.
		"""
		if row < 0 or row > len(self.board) - 1 or col < 0 or col > len(self.board[0]) - 1:
			raise IndexError
		if self.board[row][col] != self.PLACE_HOLDER:
			return self.board[row][col]
		else:
			return None

	def set_turn(self, is_my_turn: bool):

		self.__turn = is_my_turn

	def get_current_player(self):
		"""
		:return: which player is playing right now.
		"""
		if self.__turn:
			return self.PLAYER_ONE
		else:
			return self.PLAYER_TWO

	def print_board(self):
		"""
		this func is for inter use.
		:return:
		"""
		board_to_print = numpy.matrix(self.board)
		print(board_to_print)
