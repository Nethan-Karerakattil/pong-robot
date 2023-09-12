import airhockey_bot
import pygame
import random
import math

pygame.init()
pygame.font.init()
pygame.display.set_caption("Pong")

# Constants
FRAME_RATE = 60
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 512

BAT_WIDTH = 30
BAT_HEIGHT = 100
BAT_SPEED = 5

BALL_SIZE = 10
BALL_BORDER = 5
BALL_SPEED = 3

# Variables
score = [0, 0]

bat_1 = [
    BAT_WIDTH,
    SCREEN_HEIGHT / 2 - BAT_HEIGHT / 2
]
bat_2 = [
    SCREEN_WIDTH - BAT_WIDTH * 2,
    SCREEN_HEIGHT / 2 - BAT_HEIGHT / 2
]

ball_pos = [
    SCREEN_WIDTH / 2,
    SCREEN_HEIGHT / 2
]

ball_dx = random.choice((BALL_SPEED, -BALL_SPEED))
ball_dy = random.choice((BALL_SPEED, -BALL_SPEED))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("arial", 30)
clock = pygame.time.Clock()

# Main loop
while True:
    
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        mods = pygame.key.get_mods()
        if mods & pygame.KMOD_CTRL:
            if event.key == pygame.K_w:
                pygame.quit()
                exit()

    # Keyboard events
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:

        bat_1[1] -= BAT_SPEED

    if keys[pygame.K_s]:
        bat_1[1] += BAT_SPEED

    # Call bot function
    ipt = airhockey_bot.bot(ball_pos, bat_2, BAT_HEIGHT)
    if ipt == -1:
        bat_2[1] -= BAT_SPEED
    elif ipt == 1:
        bat_2[1] += BAT_SPEED

    # Move ball
    ball_pos[0] += ball_dx
    ball_pos[1] += ball_dy

    # Border collision
    if ball_pos[0] < 0 or ball_pos[0] > SCREEN_WIDTH:
        ball_pos[0] = SCREEN_WIDTH / 2
        ball_pos[1] = SCREEN_HEIGHT / 2
        ball_dx = random.choice((BALL_SPEED, -BALL_SPEED))
        ball_dy = random.choice((BALL_SPEED, -BALL_SPEED))

    if ball_pos[1] < 0 or ball_pos[1] > SCREEN_HEIGHT:
        ball_dy = -ball_dy

    # Bat collision
    def detectCollision(c, cr, r, rh, rw):
        testX = c[0]
        testY = c[1]

        if c[0] < r[0]:
            testX = r[0]
        elif c[0] > r[0] + rw:
            testX = r[0] + rw

        if c[1] < r[1]:
            testY = c[0]
        elif c[1] > r[1] + rh:
            testY = r[1] + rh

        distX = c[0] - testX
        distY = c[1] - testY
        dist = math.sqrt(distX ** 2 + distY ** 2)

        if dist <= cr:
            return True
        return False

    if detectCollision(ball_pos, BALL_SIZE, bat_1, BAT_HEIGHT, BAT_WIDTH):
        ball_dx = -ball_dx
    elif detectCollision(ball_pos, BALL_SIZE, bat_2, BAT_HEIGHT, BAT_WIDTH):
        ball_dx = -ball_dx

    # Draw elements
    screen.fill((0, 0, 0))
    pygame.draw.line(screen, pygame.Color(255, 255, 255, a=255), (SCREEN_WIDTH / 2, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    p1_score = font.render(str(score[0]), False, (255, 255, 255))
    p2_score = font.render(str(score[1]), False, (255, 255, 255))

    screen.blit(p1_score, (SCREEN_WIDTH / 2 - 70, 20))
    screen.blit(p2_score, (SCREEN_HEIGHT / 2 + 50, 20))

    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(bat_1[0], bat_1[1], BAT_WIDTH, BAT_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(bat_2[0], bat_2[1], BAT_WIDTH, BAT_HEIGHT))

    pygame.draw.circle(screen, (255, 255, 255), (ball_pos[0], ball_pos[1]), BALL_SIZE, BALL_BORDER)

    # Update screen and wait till next frame
    pygame.display.update()
    clock.tick(FRAME_RATE)
