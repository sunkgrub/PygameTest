import pygame
from sys import exit
from random import randint

def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 1000
    score_surf = test_font.render(f"Score: {current_time}", False, (64,64,64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5
            screen.blit(snail_surf, obstacle_rect)
        return obstacle_list
    else:
        return []

# Initialize the game
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((800, 400))
screen_rect = screen.get_rect()

pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
gameActive = False
start_time = 0
score = 0

sky_surface = pygame.image.load('graphics/sky.png').convert()

ground_surface = pygame.image.load('graphics/ground.png').convert()
ground_rect = ground_surface.get_rect(bottom=400)

score_surf = test_font.render('My game', False, (64,64,64),)
score_rect = score_surf.get_rect(center=(400,50))

snail_surf = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(600, ground_rect.top))

obstacle_rect_list = []

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

# Intro Graphics
player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=screen_rect.center)

game_name = test_font.render("Pixel Runner", False, (111,196,169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render("Press space to run", False, (111,196,169))
game_message_rect = game_message.get_rect(center=(400, 320))

#Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
        if gameActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_rect.bottom >= ground_rect.top:
                        player_gravity = -20
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -20
            
            if event.type == obstacle_timer:
                obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), ground_rect.top)))
                print("Snail!")
                print(obstacle_rect_list)
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.midbottom = (600, ground_rect.top)
                player_rect.midbottom = (80, 300)
                player_gravity = 0
                score = 0
                gameActive = True
                start_time = pygame.time.get_ticks()


    if gameActive:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, ground_rect)
        
        # pygame.draw.rect(screen, '#c0e8ec', score_rect,)
        # border_rect = score_rect.inflate(12, 12)
        # pygame.draw.rect(screen, '#c0e8ec', border_rect, 10)
        # screen.blit(score_surf, score_rect)

        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > ground_rect.top:
            player_rect.bottom = ground_rect.top
        screen.blit(player_surf, player_rect)

        # Obstacle movement
        object_rec_list = obstacle_movement(obstacle_rect_list)

        # collision
        if snail_rect.colliderect(player_rect):
            gameActive = False

        score = display_score()

    else:
        screen.fill((94,129,162))
        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand, player_stand_rect)
        
        score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)