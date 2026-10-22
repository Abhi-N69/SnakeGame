import sys
import random
import sqlite3
import pygame

DB_FILE = 'snake_game.db'


# ---------- Database ----------
def setup_database():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL
            )
        ''')


def insert_score(player_name, score):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            'INSERT INTO scores (player_name, score) VALUES (?, ?)',
            (player_name, score)
        )


def get_top_scores(limit=5):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            'SELECT player_name, score FROM scores ORDER BY score DESC LIMIT ?',
            (limit,)
        )
        return cur.fetchall()


setup_database()


# ---------- Game settings ----------
snake_speed = 15
window_x = 720
window_y = 480

black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)

pygame.init()
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()


# ---------- Game state ----------
snake_position = []
snake_body = []
fruit_position = []
direction = 'RIGHT'
change_to = 'RIGHT'
score = 0


def spawn_fruit():
    while True:
        pos = [
            random.randrange(0, window_x // 10) * 10,
            random.randrange(0, window_y // 10) * 10
        ]

        if pos not in snake_body:
            return pos


def reset_game():
    global snake_position, snake_body, fruit_position
    global direction, change_to, score

    snake_position = [100, 50]
    snake_body = [
        [100, 50],
        [90, 50],
        [80, 50],
        [70, 50]
    ]

    direction = 'RIGHT'
    change_to = 'RIGHT'
    score = 0

    fruit_position = spawn_fruit()


def show_score(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render(
        'Score : ' + str(score), True, color
    )
    game_window.blit(score_surface, score_surface.get_rect())


def display_leaderboard():
    top_scores = get_top_scores(5)

    font = pygame.font.Font(None, 24)
    title = font.render('LEADERBOARD:', True, white)

    game_window.blit(
        title,
        (window_x / 2 - 60, 190)
    )

    for rank, (name, sc) in enumerate(top_scores, start=1):
        line = font.render(
            f"{rank}. {name}: {sc}", True, white
        )

        game_window.blit(
            line,
            (window_x / 2 - 60, 190 + rank * 28)
        )


def game_over():
    player_name = ""

    font = pygame.font.Font(None, 32)
    input_box = pygame.Rect(
        window_x // 2 - 100, 100, 200, 40
    )

    color = pygame.Color('dodgerblue2')

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    insert_score(
                        player_name.strip() or "Anonymous",
                        score
                    )
                    reset_game()
                    return

                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]

                elif (
                    event.unicode.isprintable()
                    and len(player_name) < 12
                ):
                    player_name += event.unicode

        game_window.fill(black)

        msg = font.render(
            f'Game Over! Score: {score}. Enter your name:',
            True,
            red
        )

        game_window.blit(
            msg,
            (window_x // 2 - msg.get_width() // 2, 50)
        )

        text_surface = font.render(
            player_name, True, color
        )

        pygame.draw.rect(
            game_window, color, input_box, 2
        )

        game_window.blit(
            text_surface,
            (input_box.x + 5, input_box.y + 8)
        )

        display_leaderboard()

        pygame.display.flip()
        fps.tick(30)


# ---------- Main loop ----------
reset_game()

while True:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                change_to = 'UP'

            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'

            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'

            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'


    # Prevent reversing direction
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'

    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'

    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'

    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'


    # ---------- Move the snake ----------
    if direction == 'UP':
        snake_position[1] -= 10

    if direction == 'DOWN':
        snake_position[1] += 10

    if direction == 'LEFT':
        snake_position[0] -= 10

    if direction == 'RIGHT':
        snake_position[0] += 10


    # ---------- Wall wrapping ----------
    # Pass through walls and appear on the opposite side
    snake_position[0] %= window_x
    snake_position[1] %= window_y


    # ---------- Self-collision ----------
    # Collision with the snake's own body still ends the game
    if snake_position in snake_body[:-1]:
        game_over()
        continue


    # ---------- Growth mechanism ----------
    snake_body.insert(0, list(snake_position))

    if snake_position == fruit_position:
        score += 10
        fruit_position = spawn_fruit()

    else:
        snake_body.pop()


    # ---------- Draw ----------
    game_window.fill(black)

    for i, pos in enumerate(snake_body):

        radius = 10 if i == 0 else 8

        pygame.draw.circle(
            game_window,
            green,
            (pos[0] + 5, pos[1] + 5),
            radius
        )

    pygame.draw.circle(
        game_window,
        red,
        (fruit_position[0] + 5, fruit_position[1] + 5),
        5
    )

    show_score(white, 'times new roman', 20)

    pygame.display.update()
    fps.tick(snake_speed)
