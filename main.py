
# MODULES
import pygame, sys
import numpy as np

# initializes pygame
pygame.init()

# ---------
# CONSTANTS
# ---------
WIDTH = 600
HEIGHT = 600
WIDTH_MIDDLE, HEIGHT_MIDDLE = WIDTH // 2, HEIGHT // 2
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
# COLORS
RED = (255, 0, 0)
BG_COLOR = (28, 167, 236)
LINE_COLOR = (11, 98, 142)
CREAM = (239, 231, 200)
BLACK = (0, 0, 0)
# FONTS
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# ------
# SCREEN
# ------
WIN = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
WIN.fill( BG_COLOR )

# -------------
# CONSOLE BOARD
# -------------
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )

# ---------
# FUNCTIONS
# ---------
def draw_lines():
	# 1 horizontal
	pygame.draw.line( WIN, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
	# 2 horizontal
	pygame.draw.line( WIN, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )

	# 1 vertical
	pygame.draw.line( WIN, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
	# 2 vertical
	pygame.draw.line( WIN, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1:
				pygame.draw.circle( WIN, CREAM, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2:
				pygame.draw.line( WIN, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( WIN, RED, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )


def mark_square(row, col, player):
	board[row][col] = player

def available_square(row, col):
	return board[row][col] == 0

def is_board_full():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False
	return True

def check_win(player):

	if is_board_full():
		winner = "No one wins!"
		draw_winner(winner)
	
	# vertical win check
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical_winning_line(col, player)
			if player == 1:
				winner = "O wins!"
			elif player == 2:
				winner = "X wins!"
			draw_winner(winner)
			

	# horizontal win check
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			if player == 1:
				winner = "O wins!"
			elif player == 2:
				winner = "X wins!"
			draw_winner(winner)

	# asc diagonal win check
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(player)
		if player == 1:
			winner = "O wins!"
		elif player == 2:
			winner = "X wins!"
		draw_winner(winner)
		

	# desc diagonal win chek
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(player)
		if player == 1:
			winner = "O wins!"
		elif player == 2:
			winner = "X wins!"
		draw_winner(winner)
		

def draw_vertical_winning_line(col, player):
	pos_X = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CREAM
	elif player == 2:
		color = RED

	pygame.draw.line( WIN, color, (pos_X, 15), (pos_X, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
	pos_Y = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CREAM
	elif player == 2:
		color = RED

	pygame.draw.line( WIN, color, (15, pos_Y), (WIDTH - 15, pos_Y), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		color = CREAM
	elif player == 2:
		color = RED

	pygame.draw.line( WIN, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		color = CREAM
	elif player == 2:
		color = RED

	pygame.draw.line( WIN, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )

def restart():
	WIN.fill( BG_COLOR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0

draw_lines()

# ---------
# VARIABLES
# ---------
player = 1
running = True

def draw_winner(text):
	draw_text = WINNER_FONT.render(text, 1, BLACK) #Text
	WIN.blit(draw_text, (WIDTH_MIDDLE - draw_text.get_width() // 2, 
	HEIGHT_MIDDLE - draw_text.get_height() // 2)) #Set text in window
	pygame.display.update() #Update
	pygame.time.delay(3000) #Pause the game
	restart()

def handle_click(clicked_row, clicked_col):
	global player
	global running
	if available_square( clicked_row, clicked_col ):
		mark_square( clicked_row, clicked_col, player )
	draw_figures()
	check_win( player )
	player = player % 2 + 1
		
# --------
# MAINLOOP
# --------
def main():
	while True:
		global player, running
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN and running:

				mouseX = event.pos[0] # x
				mouseY = event.pos[1] # y

				clicked_row = int(mouseY // SQUARE_SIZE)
				clicked_col = int(mouseX // SQUARE_SIZE)


				#HANDLE CLICK
				handle_click(clicked_row, clicked_col)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					restart()
					player = 1
					running = False
				if event.key == pygame.K_ESCAPE: 
					running = False
					sys.exit()
		pygame.display.update()

if __name__ == "__main__": #Run this main, if we running THIS file directly
	main() #Main loop
