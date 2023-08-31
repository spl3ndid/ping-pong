import pygame
import sys, random

def restart():
    global ballx, bally
    ball.center = (screen_width/2, screen_height/2)
    ballx *= random.choice((1, -1))
    bally *= random.choice((1, -1))

def opp_ai():
    global opp, oppspeed
    if opp.top < ball.y:
        opp.y += oppspeed
    if opp.bottom > ball.y:
        opp.y -= oppspeed
    if opp.top < 0:
        opp.bottom = screen_height
    if opp.bottom > screen_height:
        opp.top = 0

pygame.init()

clock = pygame.time.Clock()

score1 = 0
score2 = 0

hitsound = pygame.mixer.Sound("sound/click7.ogg")

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h - 50

screen = pygame.display.set_mode((screen_width, screen_height))

ball = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 30, 30)
player = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
opp = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)

bg_color = pygame.Color("grey12")
lightgrey = (200, 200, 200)

ballx = 7 * random.choice((1, -1))
bally = 7 * random.choice((1, -1))

pygame.display.set_caption("Pong")

playerspeed = 0
oppspeed = 7

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                playerspeed += 7
            if event.key == pygame.K_UP:
                playerspeed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                playerspeed -= 7
            if event.key == pygame.K_UP:
                playerspeed += 7
    
    screen.fill(bg_color)

    if not game_over:
        opp_ai()

        # Ball Animation 
        ball.x += ballx
        ball.y += bally
        if ball.top <= 0 or ball.bottom >= screen_height:
            bally *= -1
        if ball.left <= 0:
            score2 += 1
            restart()
        elif ball.right >= screen_width:
            score1 += 1
            restart()
        if ball.colliderect(player) or ball.colliderect(opp):
            ballx *= -1
            hitsound.play(maxtime=2000)
        
        if score1 >= 10 or score2 >= 10:
            game_over = True

    # Rendering
    font = pygame.font.Font(None, 36)
    player_score_text = font.render(f"Player: {score1}", True, (255, 255, 255))
    opponent_score_text = font.render(f"Opponent: {score2}", True, (255, 255, 255))
    player_score_rect = player_score_text.get_rect(top=10, left=10)
    opponent_score_rect = opponent_score_text.get_rect(top=10, right=screen_width - 10)
    screen.blit(player_score_text, player_score_rect)
    screen.blit(opponent_score_text, opponent_score_rect)

    # Player Animation
    player.y += playerspeed
    if player.top < 0:
        player.bottom = screen_height
    if player.bottom > screen_height:
        player.top = 0
    
    # Other rendering and display code
    pygame.draw.rect(screen, lightgrey, player)
    pygame.draw.rect(screen, lightgrey, opp)
    pygame.draw.ellipse(screen, lightgrey, ball)
    pygame.draw.aaline(screen, lightgrey, (screen_width/2, 0), (screen_width/2, screen_height))

    if game_over:
        font = pygame.font.Font(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(game_over_text, game_over_rect)

    pygame.display.flip()
    clock.tick(60)
