
#!/usr/bin/env python3

from guizero import App, Box, PushButton, Text, Picture
from array import *
from random import *
from emoji import * 
import os
import sys

#game constants
WIDTH = 20
HEIGHT = 20
DIFICULTY = 1 # 1 - 5

		
#subclassing the Picture widget from guizero to add additional functionality	
class PictureButton(Picture):
	def __init__(self, master, image=None, grid=None, align=None, visible=True, enabled=None, width=None, height=None):
		
		Picture.__init__(self, master, image, grid, align, visible, enabled, width, height)
		self.pressed = False
		self.flagged = False
	
	def display_image(self, enum):
		self.image = enum
	
	def display_image_for(self, string):
		picture = EmojiImage.picture_from(string)
		self.image = picture
	

NUMBER_OF_BOMBS = WIDTH * DIFICULTY
flag_mode = False 

# 2D array to hold the game map
gamemap = [["" for j in range(HEIGHT)] for i in range(WIDTH)]


def make_board(): # creates UI of the game board
	new_board = [[None for j in range(HEIGHT)] for i in range(WIDTH)]
	global box
	for x in range(WIDTH):
		for y in range(HEIGHT):
			tile = PictureButton(box, image = EmojiImage.EMPTY.value, grid = [x, y], width = 20, height = 20)
			tile.when_clicked = tile_pressed
			new_board[x][y]= tile
	spread_bombs()
	return new_board


def spread_bombs(): # places bombs randomly on the game map
	for i in range(NUMBER_OF_BOMBS):
		xx = randint(0,WIDTH-1)
		yy = randint(0,HEIGHT-1)
		gamemap[xx][yy] = "ó"
		
	for x in range(WIDTH): # adding hints to the map - numbers with bombs arounds a spot
		for y in range(HEIGHT):
			gamemap[x][y] = nbr_of_bomb_around(x, y)
			
def bomb_on(x,y):  #return 0 or 1, depending if there is bomb on the spot or not
	if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
		if gamemap[x][y] == "ó":
			return 1
	return 0

def nbr_of_bomb_around(x, y): # counts all the bomps around given spot (x, y)
	if gamemap[x][y] == "ó":
		return "ó"
	tile_num = 0
	tile_num = bomb_on(x-1, y-1) + bomb_on(x, y-1) + bomb_on(x + 1, y - 1) + bomb_on(x - 1, y) + bomb_on(x + 1, y) + bomb_on(x + 1, y + 1) + bomb_on(x, y + 1) + bomb_on(x - 1, y + 1) 
	
	if tile_num > 0:
		return str(tile_num)
	else:
		return ""


def restart(): # geme restart
	for x in range(WIDTH):
		for y in range(HEIGHT):
			board_squares[x][y].pressed = False
			board_squares[x][y].image = EmojiImage.EMPTY.value
			gamemap[x][y] = ""
	spread_bombs()
	message.value = ""
	
	
def display_all(): # displays all tiles on the game boards (this is when you lose or win the game)
	for x in range(WIDTH):
		for y in range(HEIGHT):
			if gamemap[x][y] == "":
				gamemap[x][y] = "_"
			board_squares[x][y].display_image_for(gamemap[x][y])
			board_squares[x][y].pressed = True
			
def check_win(): #checking if game is over and if you won
	active_tiles = 0 
	for x in range(WIDTH):
		for y in range(HEIGHT):
			tile = board_squares[x][y]
			if tile.pressed == False:
				active_tiles += 1
				if not gamemap[x][y] == "ó":
					return
	if active_tiles == 0:
		message.value = "You lost!"
	else:
		message.value = "You won!"
	display_all()								
	
	
def tile_pressed(event):  # calick on the tile 
	if event.widget.enabled == False:
		return
	c = event.widget.grid
	global flag_mode
	if flag_mode == True:
		picture_button = board_squares[c[0]][c[1]]
		if picture_button.flagged == True:
			picture_button.flagged = False
			picture_button.image = EmojiImage.EMPTY.value
		else:
			picture_button.flagged = True
			picture_button.image = EmojiImage.FLAG.value
		return
	else:
		check_tile(c[0], c[1])
		check_win()

		
def flag_pressed(): #settin flag mode
	global flag_mode
	discover_button.enable()
	flag_button.disable()
	flag_mode = True
	
	
def discover_pressed(): #setting discovery mode
	global flag_mode
	flag_button.enable()
	discover_button.disable()
	flag_mode = False
	
	
def check_tile(x, y): # chaking waht's hidden under the tile you have pressed
	if x >= 0 and x < WIDTH and y >= 0 and y < HEIGHT:
		tile = board_squares[x][y]
		if tile.pressed == False: 
			if gamemap[x][y] == "": # empty filed so:
				gamemap[x][y] = "_" # 1. make it pressed on the game map
				tile.display_image(EmojiImage.PRESSED.value)
				tile.pressed = True # 2. make it pressed UI-wise
				check_tile(x + 1, y) # 3. recursivelly check all the spots around.
				check_tile(x + 1, y + 1)
				check_tile(x, y + 1)
				check_tile(x - 1, y + 1)
				check_tile(x - 1, y)				
				check_tile(x - 1, y - 1)
				check_tile(x, y - 1)
				check_tile(x + 1, y - 1)
			elif gamemap[x][y] == "ó": # there is a BOMB - you lose
				# bomb
				display_all()
			else:
				# otherwise there must be number, a hint, so display ony that hint.
				board_squares[x][y].display_image_for(gamemap[x][y])
				board_squares[x][y].pressed = True

# UI
app = App("Minesweeper by Wojciech Kosikowski", width = WIDTH * 25 + 40, height= HEIGHT * 25 + 150)
message = Text(app, text="Select a tile you think is not mined")

box = Box(app, layout = "grid")
board_squares = make_board()


buttons = Box(app, layout = "grid")
discover_button = PushButton(buttons, text = "Discover", grid = [1,0], width = 18, height = 18, image = EmojiImage.DISCOVER.value ,command = discover_pressed, enabled = False)

flag_button = PushButton(buttons,width = 18, height = 18, grid = [2,0], image = EmojiImage.FLAG.value ,command = flag_pressed)
restart_button = PushButton(buttons, image = "Images/repeat.png",width = 18, height = 18, grid = [3,0],  command = restart)

app.display()
