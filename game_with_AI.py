'''
In this script we are going to program the game 4connect but with the AI

The inspiration came from the video https://www.youtube.com/watch?v=UYgyRArKDEs&list=PLFCB5Dp81iNV_inzM-R9AKkZZlePCZdtV from Keith Galli

I use pygame, and minimax algorithm as AI.


Author: Leonardo Ferigutti

January 2021

'''

import numpy as np
import pygame
import sys
import math
import random



## Global Constant

ROW_COUNT = 6
COL_COUNT = 7
game_over = False
valid_move = True
SQUARESIZE = 100
WIDTH = COL_COUNT * SQUARESIZE
HEIGHT = (ROW_COUNT +1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)
BOARD_COLOR = (23,93,222)
SCREEN_COLOR = (8,0,0)
PLAYER_1_COLOR =  (255,0,0)
PLAYER_1_COLOR_DARK =  (200,0,0)
PLAYER_2_COLOR = (255,240,0)
PLAYER_2_COLOR_DARK = (205,190,0)
RADIUS = int((SQUARESIZE)/2-7)
PLAYER = 1
AI = 2
turn = 1
posx = 0
WINDOW_LENGHT = 4
EMPTY = 0
AI_PIECE = 2
PLAYER_PIECE = 1
PLAYER_2 = 3
HUMAN_VS_HUMAN = False
first_game = True
DEPTH = 2

## Funcionalities

def create_board():
	empty_board  = np.zeros((ROW_COUNT,COL_COUNT))
	return empty_board


def next_row_available(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r
			break


def evaluate_window(window,piece):
	score = 0
	opp_piece = PLAYER_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(EMPTY) ==1:
		score += 10
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += 5

	if window.count(opp_piece) == 3 and window.count(EMPTY) ==1:
		score -= 80

	#elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
	#	score -= 20
	return score


def is_terminal_node(board):

	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_location(board))==0


def minimax_algorithm(board,depth,alpha,beta,maxmizingPlayer):
	valid_locations = get_valid_location(board)

	if depth == 0 or is_terminal_node(board):
		if is_terminal_node:
			if winning_move(board,AI_PIECE):
				return (None, math.inf)
			elif winning_move(board,PLAYER_PIECE):
				return(None,-math.inf)
			else: 
				return (None, board_posicion_score(board,AI_PIECE))

	if maxmizingPlayer:
		value = -math.inf
		best_col = random.choice(valid_locations)
		for col in valid_locations:
			row = next_row_available(board,col)
			new_board = board.copy()
			drop_piece(new_board,row,col,AI_PIECE)
			new_score = minimax_algorithm(new_board,depth-1,alpha,beta,False)[1]
			#print('AI -- Col {}, Value {}'.format(col,new_score))
			
			if new_score > value:
				value = new_score
				best_col = col
			alpha = max(alpha,value)
			if alpha >= beta:
				break
		return best_col, value

	else: # Minimazing player
		value = math.inf
		best_col = random.choice(valid_locations)
		for col in valid_locations:
			row = next_row_available(board,col)
			new_board = board.copy()
			drop_piece(new_board,row,col,PLAYER_PIECE)
			new_score =minimax_algorithm(new_board,depth-1,alpha,beta,True)[1]
			#print('PLAYER -- Col {}, Value {}'.format(col,new_score))
			
			if new_score < value:
				value = new_score
				best_col = col
			beta = min(beta,value)
			if beta <=alpha:
				break
		
		return best_col, value


def board_posicion_score(board, piece):
	score = 0
	
	# Score center
	center_array = [int(i) for i in list(board[:,COL_COUNT//2])]
	center_count = center_array.count(piece)
	score += center_count *4



	# Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in board[r,:]]
		for c in range(COL_COUNT-3):
			window = row_array[c:c+WINDOW_LENGHT]
			score += evaluate_window(window,piece)

	
	# Score Vertical
	for c in range(COL_COUNT):
		col_array = [int(i) for i in board[:,c]]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGHT]
			score += evaluate_window(window,piece)


	# Score diagonal positive
	for r in range(ROW_COUNT-3):
		for c in range(COL_COUNT-3):
			window = [board[r+i][c+i] for i in range(WINDOW_LENGHT)]
			score += evaluate_window(window,piece)

	# Score diagonal negative
	for r in range(3,ROW_COUNT):
		for c in range(COL_COUNT-3):
			window = [board[r-i][c+i] for i in range(WINDOW_LENGHT)]
			score += evaluate_window(window,piece)
	return score


def get_valid_location(board):
	valid_locations = []
	for col in range(COL_COUNT):
		if board[ROW_COUNT-1][col] == 0:
			valid_locations.append(col)
	return valid_locations


def get_best_col(board, piece):
	

	valid_locations = get_valid_location(board)
	best_score = -10000
	best_col = random.choice(valid_locations)
	for col in valid_locations:
		row = next_row_available(board,col)
		new_board = board.copy()
		new_board = drop_piece(new_board,row,col,piece)
		score = board_posicion_score(new_board,piece)
		if score > best_score:
			best_score = score
			best_col = col

	return best_col


def drop_piece(board,row,col,piece):
	board[row][col] = piece
	return board


def draw_board(board):
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen,BOARD_COLOR,(c*SQUARESIZE, (r+1)*SQUARESIZE,SQUARESIZE,SQUARESIZE))
			pygame.draw.circle(screen,SCREEN_COLOR,(int(c*SQUARESIZE+SQUARESIZE/2),r*SQUARESIZE+SQUARESIZE+int(SQUARESIZE/2)), RADIUS)

	for c in range(COL_COUNT):
		for r in range(ROW_COUNT):
			if board[r][c] == 1:
				pygame.draw.circle(screen,PLAYER_1_COLOR,(int(c*SQUARESIZE+SQUARESIZE/2),HEIGHT - int(r*SQUARESIZE+int(SQUARESIZE/2))), RADIUS)
			elif board[r][c] == 2:
				pygame.draw.circle(screen,PLAYER_2_COLOR,(int(c*SQUARESIZE+SQUARESIZE/2),HEIGHT - int(r*SQUARESIZE+int(SQUARESIZE/2))), RADIUS)

	pygame.display.update()			
	

def draw_menu():

	pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
	pygame.draw.rect(screen,PLAYER_1_COLOR_DARK,(WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
	pygame.draw.rect(screen,PLAYER_2_COLOR_DARK,(WIDTH/2 + WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
	label = myfont2.render('Click on the screen to START',True,PLAYER_1_COLOR)
	screen.blit(text_player,(WIDTH/5.5,SQUARESIZE-SQUARESIZE/2))
	screen.blit(text_AI,(WIDTH/2 + WIDTH/4.5,SQUARESIZE-SQUARESIZE/2))
	screen.blit(label,(100,10))
	
 
	pygame.display.update()	
	 


def winning_move(board, player):
	# Horizontal winning

	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == player and board[r][c+1] == player and board[r][c+2] == player and board[r][c+3] == player:
				return True
			
	# Vertical winning
	for c in range(COL_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == player and board[r+1][c] == player and board[r+2][c] == player and board[r+3][c] == player:
				return True
			

	# Positive Diagonal winning
	for c in range(COL_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == player and board[r+1][c+1] == player and board[r+2][c+2] == player and board[r+3][c+3] == player:
				return True

	# Negative Diagonal winning				
	for c in range(COL_COUNT-3):
		for r in range(3,ROW_COUNT):
			if board[r][c] == player and board[r-1][c+1] == player and board[r-2][c+2] == player and board[r-3][c+3] == player:
				return True


def draw_difficulty():

	#screen.blit(easy_text,(WIDTH/2 - WIDTH/8,HEIGHT/+SQUARESIZE+SQUARESIZE/2))
	pygame.draw.rect(screen,PLAYER_2_COLOR_DARK,(WIDTH/2-WIDTH/8,SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
	screen.blit(easy_text,(WIDTH/2-40,SQUARESIZE+SQUARESIZE/3))
	pygame.draw.rect(screen,PLAYER_2_COLOR_DARK,(WIDTH/2-WIDTH/8,2*SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
	screen.blit(medium_text,(WIDTH/2-40,2*SQUARESIZE+SQUARESIZE/3))
	pygame.draw.rect(screen,PLAYER_2_COLOR_DARK,(WIDTH/2-WIDTH/8,3*SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
	screen.blit(hard_text,(WIDTH/2-40,3*SQUARESIZE+SQUARESIZE/3))
	pygame.draw.rect(screen,PLAYER_2_COLOR_DARK,(WIDTH/2-WIDTH/8,4*SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
	screen.blit(insane_text,(WIDTH/2-40,4*SQUARESIZE+SQUARESIZE/3))
	pygame.display.update()		

##  Game looop

while True :

	# Inicialization of the screen, board and fonts
	

	board = create_board()
	pygame.init()
	screen = pygame.display.set_mode(SIZE)
	myfont = pygame.font.SysFont('monospace',75)
	myfont2 = pygame.font.SysFont('monospace',30)
	text_player = myfont2.render('Human',True,SCREEN_COLOR)
	text_AI = myfont2.render('AI',True,SCREEN_COLOR)
	easy_text = myfont2.render('Easy',True,SCREEN_COLOR)
	medium_text = myfont2.render('Medium',True,SCREEN_COLOR)
	hard_text = myfont2.render('Hard',True,SCREEN_COLOR)
	insane_text = myfont2.render('Insane',True,SCREEN_COLOR)
	

	# Drawing Menu and choosing dificulty
	while first_game:
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			draw_menu()
			mouse = pygame.mouse.get_pos()

			if WIDTH/8 <= mouse[0] <= WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3: 
				
				pygame.draw.rect(screen,PLAYER_1_COLOR,(WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
				screen.blit(text_player,(WIDTH/5.5,SQUARESIZE-SQUARESIZE/2))
				pygame.display.update()
			elif WIDTH/2 + WIDTH/8 <= mouse[0] <= WIDTH/2 + WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3:
				pygame.draw.rect(screen,PLAYER_2_COLOR,(WIDTH/2 + WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
				screen.blit(text_AI,(WIDTH/2 + WIDTH/4.5,SQUARESIZE-SQUARESIZE/2))
				pygame.display.update()
			



			if event.type == pygame.MOUSEBUTTONDOWN:
				click_mouse = event.pos
				
				if WIDTH/8 <= click_mouse[0] <= WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= click_mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3:
					HUMAN_VS_HUMAN = True
					turn = 1
					first_game = False
				elif WIDTH/2 + WIDTH/8 <= mouse[0] <= WIDTH/2 + WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3:
					turn = random.randint(PLAYER,AI)
					HUMAN_VS_HUMAN = False
					
					
					draw_difficulty()
					while first_game:
						
						for event in pygame.event.get():
							if event.type == pygame.QUIT:
								sys.exit()
							draw_difficulty()
							mouse = pygame.mouse.get_pos()
							if WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
								pygame.draw.rect(screen,PLAYER_2_COLOR,(WIDTH/2-WIDTH/8,SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
								screen.blit(easy_text,(WIDTH/2-40,SQUARESIZE+SQUARESIZE/3))
								pygame.display.update()

							elif WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and 2*SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= 2*SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
								pygame.draw.rect(screen,PLAYER_2_COLOR,(WIDTH/2-WIDTH/8,2*SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
								screen.blit(medium_text,(WIDTH/2-40,2*SQUARESIZE+SQUARESIZE/3))
								pygame.display.update()
							
							elif WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and 3*SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= 3*SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
								pygame.draw.rect(screen,PLAYER_2_COLOR,(WIDTH/2-WIDTH/8,3*SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
								screen.blit(hard_text,(WIDTH/2-40,3*SQUARESIZE+SQUARESIZE/3))
								pygame.display.update()
							
							elif WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and 4*SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= 4*SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
								pygame.draw.rect(screen,PLAYER_2_COLOR,(WIDTH/2-WIDTH/8,4*SQUARESIZE+SQUARESIZE/3,WIDTH/4,SQUARESIZE/3))
								screen.blit(insane_text,(WIDTH/2-40,4*SQUARESIZE+SQUARESIZE/3))
								pygame.display.update()


							if event.type == pygame.MOUSEBUTTONDOWN:
								click_mouse = event.pos

								if WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
									DEPTH = 2
									first_game = False
								elif WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and 2*SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= 2*SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
									DEPTH = 3
									first_game = False								
								elif WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and 3*SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= 3*SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
									DEPTH = 4
									first_game = False							
								elif WIDTH/2-WIDTH/8 <= mouse[0] <= WIDTH/2-WIDTH/8+WIDTH/4 and 4*SQUARESIZE+SQUARESIZE/3 <= mouse[1] <= 4*SQUARESIZE+SQUARESIZE/3+SQUARESIZE/3:
									DEPTH = 5
									first_game = False
					
	

	# Preparing the baord
	draw_board(board)
	pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
	pygame.display.update()



	# Game Itself
	while not game_over:

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			if event.type == pygame.MOUSEMOTION:
				pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
				posx = event.pos[0]
				if turn == PLAYER:
					pygame.draw.circle(screen,PLAYER_1_COLOR,(posx,int(SQUARESIZE/2)),RADIUS)
				elif turn == PLAYER_2:
					pygame.draw.circle(screen,PLAYER_2_COLOR,(posx,int(SQUARESIZE/2)),RADIUS)

			pygame.display.update()

			if event.type == pygame.MOUSEBUTTONDOWN:
				
				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))
				if board[ROW_COUNT-1][col] == 0:



					# Player 1 move
					if turn == PLAYER:

						# Movement itself
						row = next_row_available(board,col)
						board = drop_piece(board,row,col,PLAYER_PIECE)
						
						# Winning move?
						if winning_move(board,PLAYER_PIECE):
							pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
							label = myfont.render('Player 1 wins!',1,PLAYER_1_COLOR)
							screen.blit(label,(40,10))
							draw_board(board)
							pygame.time.delay(2000)
							game_over = True
						
						elif len(get_valid_location(board))==0:
							pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
							label = myfont.render('It\' a Draw',1,PLAYER_1_COLOR)
							screen.blit(label,(40,10))
							pygame.time.delay(2000)
							game_over=True


						else:	

							pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
							draw_board(board)
							pygame.display.update()
							
							if HUMAN_VS_HUMAN:
								
								pygame.draw.circle(screen,PLAYER_2_COLOR,(posx,int(SQUARESIZE/2)),RADIUS)
								pygame.display.update()
								turn = PLAYER_2
							else:
							 	turn = AI	

					elif turn == PLAYER_2:



						# Movement itself
						row = next_row_available(board,col)
						board = drop_piece(board,row,col,AI_PIECE)
						
						if winning_move(board,AI_PIECE):
							label = myfont.render('Player 2 wins!',1,PLAYER_2_COLOR)
							screen.blit(label,(40,10))
							draw_board(board)
							pygame.time.delay(2000)
							game_over = True
						
						elif len(get_valid_location(board))==0:
							pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
							label = myfont.render('It\' a Draw',1,PLAYER_1_COLOR)
							screen.blit(label,(40,10))
							pygame.time.delay(2000)
							game_over=True

						else: 
							pygame.draw.circle(screen,PLAYER_1_COLOR,(posx,int(SQUARESIZE/2)),RADIUS)
							pygame.display.update()
							#draw_board(board)
							turn = 1

		# AI move
		if turn == AI:
		
			#AI Thinking
				

			col, minmax_score = minimax_algorithm(board,DEPTH,-math.inf,math.inf,True)


			# Movement
			row = next_row_available(board,col)
			board = drop_piece(board,row,col,AI_PIECE)
			pygame.time.wait(500)
			
			
			if winning_move(board,AI_PIECE):
				label = myfont.render('AI wins!',1,PLAYER_2_COLOR)
				screen.blit(label,(WIDTH/4,10))
				draw_board(board)
				pygame.time.delay(2000)
				game_over = True

			elif len(get_valid_location(board))==0:
				pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
				label = myfont.render('It\' a Draw',1,PLAYER_1_COLOR)
				screen.blit(label,(40,10))
				pygame.time.delay(2000)
				game_over=True
			
			else: 
				pygame.draw.circle(screen,PLAYER_1_COLOR,(posx,int(SQUARESIZE/2)),RADIUS)
				pygame.display.update()
				turn = 1
		
			
		






		

		draw_board(board)


	# Play again or exit (Not able to change AI level - Only in the Menu)
	while game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()


			
			pygame.draw.rect(screen,SCREEN_COLOR,(0,0,WIDTH,SQUARESIZE))
			pygame.draw.rect(screen,PLAYER_1_COLOR_DARK,(WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
			pygame.draw.rect(screen,PLAYER_2_COLOR_DARK,(WIDTH/2 + WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
			label = myfont2.render('Click on the screen to play again',True,PLAYER_1_COLOR)
			screen.blit(text_player,(WIDTH/5.5,SQUARESIZE-SQUARESIZE/2))
			screen.blit(text_AI,(WIDTH/2 + WIDTH/4.5,SQUARESIZE-SQUARESIZE/2))
			screen.blit(label,(40,10))

			pygame.display.update()

			mouse = pygame.mouse.get_pos() 
			      
			 # if mouse is hovered on a button it 
			 # changes to lighter shade  
			if WIDTH/8 <= mouse[0] <= WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3: 
				
				pygame.draw.rect(screen,PLAYER_1_COLOR,(WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
				screen.blit(text_player,(WIDTH/5.5,SQUARESIZE-SQUARESIZE/2))
				pygame.display.update()
			elif WIDTH/2 + WIDTH/8 <= mouse[0] <= WIDTH/2 + WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3:
				pygame.draw.rect(screen,PLAYER_2_COLOR,(WIDTH/2 + WIDTH/8,SQUARESIZE-SQUARESIZE/2,WIDTH/4,SQUARESIZE/3))
				screen.blit(text_AI,(WIDTH/2 + WIDTH/4.5,SQUARESIZE-SQUARESIZE/2))
				pygame.display.update()
			



			if event.type == pygame.MOUSEBUTTONDOWN:
				click_mouse = event.pos
				
				if WIDTH/8 <= click_mouse[0] <= WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= click_mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3:
					HUMAN_VS_HUMAN = True
					turn = 1
					game_over = False
				elif WIDTH/2 + WIDTH/8 <= mouse[0] <= WIDTH/2 + WIDTH/8+WIDTH/4 and SQUARESIZE-SQUARESIZE/2 <= mouse[1] <= SQUARESIZE-SQUARESIZE/2+SQUARESIZE/3:
					turn = random.randint(PLAYER,AI)
					HUMAN_VS_HUMAN = False
					game_over = False

	