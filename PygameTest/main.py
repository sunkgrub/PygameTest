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
            if obstacle_rect.bottom == fly_height:
                screen.blit(fly_surf, obstacle_rect)
            else:
                screen.blit(snail_surf, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100 ]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
            
    return True

def player_animation():
    global player_index, player_surf

    if player_rect.bottom < ground_rect.top:
        player_surf = player_jump
    else:
        player_index += 0.1
        player_surf = player_walk[int(player_index) % 2]

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


# Snail
snail_frame_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('graphics/fly/fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('graphics/fly/fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_height = 140
fly_frame_index = 0
fly_surf = fly_frames[snail_frame_index]


obstacle_rect_list = []

player_walk1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk1, player_walk2]
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_index = 0

player_surf = player_walk[player_index]
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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

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
                if randint(0,2):
                    obstacle_rect_list.append(fly_surf.get_rect(bottomright=(randint(900, 1100), fly_height)))
                else:
                    obstacle_rect_list.append(snail_surf.get_rect(bottomright=(randint(900, 1100), ground_rect.top)))
            
            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            
            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
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
        player_animation()


        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # collisions
        gameActive = collisions(player_rect, obstacle_rect_list)

        # Score
        score = display_score()

    else:
        obstacle_rect_list.clear()

        screen.fill((94,129,162))
        screen.blit(game_name, game_name_rect)
        screen.blit(player_stand, player_stand_rect)

        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = test_font.render(f"Your score: {score}", False, (111,196,169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)