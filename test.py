import tools
import time
import random

class Point(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return "x: {}, y: {}".format(self.x, self.y)
	def __eq__(self, other):
		return str(self) == str(other)
	def __repr__(self):
		return "Point({}, {})".format(self.x, self.y)	

rect_size = Point(15,15)
food = Point(random.randint(2, 14), random.randint(2, 14))
snake = [Point(1,1), Point(2,1), Point(3,1), Point(4,1)]
empty_loop = 0

	
def control_input(previous_input):
	direction = previous_input
	dir_input = tools.get_key()
	if dir_input == 'w':
		direction = 'up'
	elif dir_input == 's':
		direction = 'down'	
	elif dir_input == 'a':
		direction = 'left'
	elif dir_input == 'd':
		direction = 'right'
	return direction	

def maybe_eat_food_and_grow():
	global snake
	global food
	if snake[0] == food:
		food = Point(random.randint(2, 14), random.randint(2, 14))
		return True
		
def game_border():
	global snake
	global rect_size
	if snake[0].y == - 1 or snake[0].x == -1 or (snake[0].y == rect_size.y) or (snake[0].x == rect_size.x):
		return False
	else:
		return True

def snake_overlay():
	global snake
	snake_head = snake[0]
	snake_body = snake[1:]
	if not (snake_head in snake_body):
		return True
	else:
		return False	

def scores_tupple():
	global scores
	z = 0
	for string in read_scores():
		string_without_newline = string[:-1]	
		string = string_without_newline.split(",")
		string = (int(string[0]), string[1])
		scores.insert(z, string)
		z += 1



def score():
	global snake
	global score_points
	score_points = ((len(snake) * 10)-40)
	#return score_points

def get_player_name():
	global player
	print "ENTER YOUR NAME:"
	player_name = raw_input()
	player = player_name

def leaderboard():
	global scores
	print "LEADERBORD"
	print ""
	for elem in scores:
		print str(elem[1]) + " scored " + str(elem[0]) + " points!"


scores = []	
score_points = 0
player = ""

def add_result():
	global score_points
	global player
	global scores	
	score_plus_name = (score_points, player)
	scores.insert(find_element(), score_plus_name)
	

	
def find_element():
	global score_points
	global scores
	total = 0
	if len(scores) > 0:
		for x in scores:
			if score_points < x[0]:
				total += 1
		else:
			return total
	else:
		return 0	

def save_scores():
	global scores
	scores_file = open("snake_scores.txt", "w")
	for x in scores:
		scores_file.write(str(x[0]) + "," + (str(x[1])) + "\n")	

def read_scores():
	scores_file = open("snake_scores.txt", "r")
	return scores_file.readlines()

def board_max_10():
	global scores
	if len(scores) > 9:
		scores.pop()



def move_snake(snake, direction):
	vel_x = 0
	vel_y = 0
	if direction == 'up':
		vel_x, vel_y = 0, -1
	if direction == 'down':
		vel_x, vel_y = 0, 1
	if direction == 'left':
		vel_x, vel_y = -1, 0
	if direction == 'right':
		vel_x, vel_y = 1, 0	

	snake_new_head = Point(snake[0].x + vel_x, snake[0].y + vel_y)
	snake.insert(0, snake_new_head)
	if not maybe_eat_food_and_grow():
		snake.pop()

def is_point_in_snake(point, snake):

	for seq in snake:
		if seq == point:
			return True
	return False			

def draw_frame(rect_size, food, snake):
	print '+' + ('-' * rect_size.x) + '+'
	for y in range(rect_size.y):
		line = '|'
		for x in range(rect_size.x):
			cur_point = Point(x, y)
			if cur_point == snake[0]:
				line += '@'
			elif is_point_in_snake(cur_point, snake):
				line += '#'
			elif cur_point == food:
				line += '*'
			else: 
				line += ' '	
		line += '|'		
		print line	
	print '+' + ('-' * rect_size.x) + '+'		



def game_loop():
    scores_tupple()
    direction = 'down' # snake moves down at game start
    size = rect_size
    global snake
    global food
    while game_border() and snake_overlay():
    	
        direction = control_input(direction)
        move_snake(snake, direction)
        tools.clear_screen()
        draw_frame(size, food, snake)
        maybe_eat_food_and_grow()
        score()
        print score_points
        time.sleep(0.250)
    else:
    	print "GAME OVER"
    	get_player_name()
    	board_max_10()
    	add_result()
    	leaderboard()
    	save_scores()    

game_loop()

