import pygame
import random
pygame.init()

# Set up display
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Pong Game MF!")

# VAriables
timer = pygame.time.Clock()
font = pygame.font.Font(None, 30)
frame_rate = 60
game_over = False
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
ball_color = white
hit_timer = 0
player_y = 130
player_speed = 4
computer_y = 130
player_direction = 0
ball_x = 145
ball_y = 145
ball_x_direction = 1
ball_y_direction = 1
ball_speed = 2
ball_y_speed = 2
score = 0
ball_color = white

# AI movement function


def update_ai(ball_y, computer_y):
    computer_speed = 3
    if computer_y + 15 < ball_y + 5:
        computer_y += computer_speed
    elif computer_y + 15 > ball_y + 5:
        computer_y -= computer_speed
    return computer_y

# Ball movement function


def update_ball(ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed):
    # Horizontal movement
    if ball_x_direction == 1:
        ball_x += ball_speed
    else:
        ball_x -= ball_speed

    # Vertical movement
    if ball_y_direction == 1:
        ball_y += ball_y_speed
    else:
        ball_y -= ball_y_speed

    # Vertical bounds check
    if ball_y <= 0 or ball_y >= 290:
        ball_y_direction *= -1
        # Keep ball in bounds
        ball_y = max(0, min(ball_y, 290))
    return ball_x_direction, ball_y_direction, ball_x, ball_y


def check_collision(ball, player, computer, ball_x_direction, score, current_color):
    """Check collisions and return updated direction, score, color and hit flag.

    Returns: (ball_x_direction, score, new_color, hit)
    """
    hit = False
    new_color = current_color
    if ball.colliderect(player) and ball_x_direction == -1:
        ball_x_direction = 1
        hit = True
        print("hit")
        score += 1
        new_color = (random.randint(120, 255), random.randint(
            120, 255), random.randint(120, 255))
    elif ball.colliderect(computer) and ball_x_direction == 1:
        ball_x_direction = -1
        hit = True
        print("hit")
    return ball_x_direction, score, new_color, hit


def check_game_over(ball_x, game_over):
    if ball_x <= 0 or ball_x >= 290 and not game_over:
        game_over = True
    return game_over


# Game loop
running = True
while running:
    timer.tick(frame_rate)
    screen.fill(black)
    game_over = check_game_over(ball_x, game_over)
    if not game_over:
        player = pygame.draw.rect(screen, white, (5, player_y, 10, 40))
    computer = pygame.draw.rect(screen, white, (285, computer_y, 10, 40))
    ball = pygame.draw.rect(screen, ball_color, [ball_x, ball_y, 10, 10])
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle player movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player_direction = -1
            if event.key == pygame.K_s:
                player_direction = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w and player_direction == -1:
                player_direction = 0
            if event.key == pygame.K_s and player_direction == 1:
                player_direction = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                # Reset game variables
                game_over = False
                ball_x = 145
                ball_y = 145
                ball_x_direction = 1
                ball_y_direction = 1
                player_y = 130
                computer_y = 130
                score = 0

    # Update player position
    player_y += player_direction * player_speed

    # Keep player in bounds
    player_y = max(0, min(player_y, 260))

    # Update computer and ball uwu :)
    if not game_over:
        computer_y = update_ai(ball_y, computer_y)
        ball_x_direction, ball_y_direction, ball_x, ball_y = update_ball(
            ball_x_direction, ball_y_direction, ball_x, ball_y, ball_speed, ball_y_speed)
        ball_x_direction, score, new_color, hit = check_collision(
            ball, player, computer, ball_x_direction, score, ball_color)
        if hit:
            hit_timer = 400
            ball_color = new_color

    # Decrease hit timer and revert color when it expires
    if hit_timer > 0:
        hit_timer -= 1
    else:
        ball_color = white
    # Display score
    score_text = font.render(f"Score: {score}", True, white, black)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("Game Over:(", True, white, black)
        screen.blit(game_over_text, (90, 130))
        restart_button = pygame.draw.rect(screen, white, [65, 160, 100, 20])
        restart_text = font.render(
            "Press to Restart", True, white, black)
        screen.blit(restart_text, (65, 160))

    # (player already moved earlier in this loop)
    ball_speed = 3 + (score // 10)
    ball_y_speed = 2 + (score // 15)

    pygame.display.flip()  # acc render all that shit or not i dont really knwo what ts dous

pygame.quit()
