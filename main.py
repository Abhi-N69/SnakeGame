import pygame
import time
import random
import sqlite3
# Database setup
def setup_database():
conn = sqlite3.connect('snake_game.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
id INTEGER PRIMARY KEY,
player_name TEXT NOT NULL,
score INTEGER NOT NULL
)
''')
conn.commit()
conn.close()
def insert_score(player_name, score):
conn = sqlite3.connect('snake_game.db')
cursor = conn.cursor()
cursor.execute('INSERT INTO scores (player_name, score) VALUES (?, ?)',
(player_name, score))
conn.commit()
conn.close()
def get_top_scores(limit=5):
conn = sqlite3.connect('snake_game.db')
cursor = conn.cursor()
cursor.execute('SELECT player_name, score FROM scores ORDER BY score DESC
LIMIT ?', (limit,))
scores = cursor.fetchall()
conn.close()
return scores
# Initialize database
setup_database()
# Game settings
snake_speed = 15
window_x = 720
window_y = 480
# Defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
# Initializing pygame
pygame.init()
# Initialize game window
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))
# FPS (frames per second) controller
fps = pygame.time.Clock()
# Defining snake default position
snake_position = [100, 50]
# Defining first 4 blocks of snake body
snake_body = [[100, 50],
[90, 50],
[80, 50],
[70, 50]
]
# Fruit position
fruit_position = [random.randrange(1, (window_x//10)) * 10,
random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True
# Setting default snake direction towards right
direction = 'RIGHT'
change_to = direction
# Initial score
score = 0
# Displaying Score function
def show_score(choice, color, font, size):
score_font = pygame.font.SysFont(font, size)
score_surface = score_font.render('Score : ' + str(score), True, color)
score_rect = score_surface.get_rect()
game_window.blit(score_surface, score_rect)
Game over function
def game_over():
global score
player_name = ""
input_active = True
input_box = pygame.Rect(window_x / 2 - 100, window_y / 2, 200, 50)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
font = pygame.font.Font(None, 32)
while input_active:
for event in pygame.event.get():
if event.type == pygame.QUIT:
pygame.quit()
quit()
if event.type == pygame.MOUSEBUTTONDOWN:
if input_box.collidepoint(event.pos):
input_active = True
else:
input_active = False
if event.type == pygame.KEYDOWN:
if input_active:
if event.key == pygame.K_RETURN:
insert_score(player_name, score) # Save score to database
input_active = False
elif event.key == pygame.K_BACKSPACE:
player_name = player_name[:-1]
else:
player_name += event.unicode
game_window.fill(black)
game_over_surface = font.render('Game Over! Enter your name:', True, red)
game_window.blit(game_over_surface, (window_x / 2 - 150, window_y / 4))
# Update the text surface for the input box
text_surface = font.render(player_name, True, color)
pygame.draw.rect(game_window, color, input_box, 2)
game_window.blit(text_surface, (input_box.x + 5, input_box.y + 5))
# Display leaderboard
display_leaderboard()
pygame.display.flip()
fps.tick(30)
def display_leaderboard():
top_scores = get_top_scores(10) # Get top 10 scores
font = pygame.font.Font(None, 24)
leaderboard_surface = font.render('LEADERBOARD:', True, white)
game_window.blit(leaderboard_surface, (window_x / 2 - 50, window_y / 2 + 60))
for rank, (name, score) in enumerate(top_scores, start=1):
score_surface = font.render(f"{rank}. {name}: {score}", True, white)
game_window.blit(score_surface, (window_x / 2 - 50, window_y / 2 + 60 + rank * 30))
# Main Function
while True:
for event in pygame.event.get():
if event.type == pygame.KEYDOWN:
if event.key == pygame.K_UP:
change_to = 'UP'
if event.key == pygame.K_DOWN:
change_to = 'DOWN'
if event.key == pygame.K_LEFT:
change_to = 'LEFT'
if event.key == pygame.K_RIGHT:
change_to = 'RIGHT'
# If two keys pressed simultaneously
if change_to == 'UP' and direction != 'DOWN':
direction = 'UP'
if change_to == 'DOWN' and direction != 'UP':
direction = 'DOWN'
if change_to == 'LEFT' and direction != 'RIGHT':
direction = 'LEFT'
if change_to == 'RIGHT' and direction != 'LEFT':
direction = 'RIGHT'
# Moving the snake
if direction == 'UP':
snake_position[1] -= 10
if direction == 'DOWN':
snake_position[1] += 10
if direction == 'LEFT':
snake_position[0] -= 10
if direction == 'RIGHT':
snake_position[0] += 10
# Snake body growing mechanism
snake_body.insert(0, list(snake_position))
if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
score += 10
fruit_spawn = False
else:
snake_body.pop()
if not fruit_spawn:
fruit_position = [random.randrange(1, (window_x//10)) * 10,
random.randrange(1, (window_y//10)) * 10]
fruit_spawn = True
game_window.fill(black)
# Draw the snake with a curved head
for i, pos in enumerate(snake_body):
if i == 0: # Head of the snake
pygame.draw.circle(game_window, green, (pos[0] + 5, pos[1] + 5), 10) # Head
else: # Body of the snake
pygame.draw.circle(game_window, green, (pos[0] + 5, pos[1] + 5), 8) # Body segments
# Draw the food as a red circle
pygame.draw.circle(game_window, red, (fruit_position[0] + 5, fruit_position[1] + 5), 5)
# Game Over conditions
if snake_position[0] < 0 or snake_position[0] > window_x - 10:
game_over()
if snake_position [1] < 0 or snake_position[1] > window_y - 10:
game_over()
# Touching the snake body
for block in snake_body[1:]:
if snake_position[0] == block[0] and snake_position[1] == block[1]:
game_over()
# Displaying score continuously
show_score(1, white, 'times new roman', 20)
# Refresh game screen
pygame.display.update()
# Frame Per Second / Refresh Rate
fps.tick(snake_speed)
