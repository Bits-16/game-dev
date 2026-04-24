import pygame
import random

pygame.init()

# System Variables
screen_width = 400
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()
run = True

# Pipes
pipes = []
pipe_time = 1200
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, pipe_time)
pipe_height = [300, 400, 500]

# Colours
bg = (135, 206, 235)
green = (80, 200, 120)

# Bird
bird_rect = pygame.Rect(100, 350, 30, 30)
bird_gravity = 0.25
bird_velocity = 0
bird_jump = -8

game_active = True
game_over = False
fade_alpha = 0
fade_speed = 5
text_alpha = 0

# Fonts
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 30)

# Score
score = 0
high_score = 0

# Load high score from file
try:
    with open("highscore.txt", "r") as f:
        high_score = int(f.read())
except FileNotFoundError:
    high_score = 0

def save_high_score():
    with open("highscore.txt", "w") as f:
        f.write(str(high_score))

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= 0 or bird_rect.bottom >= screen_height:
        return False
    return True

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, green, pipe)

def draw_bird():
    pygame.draw.rect(screen, (255, 255, 0), bird_rect)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_velocity = bird_jump
                elif game_over:
                    game_active = True
                    game_over = False
                    pipes.clear()
                    bird_rect.center = (100, 350)
                    bird_velocity = 0
                    score = 0

        if event.type == spawn_pipe:
            random_pipe_height = random.choice(pipe_height)
            gap_size = 150

            top_pipe = pygame.Rect(screen_width, 0, 50, random_pipe_height - gap_size)
            bottom_pipe = pygame.Rect(screen_width, random_pipe_height + gap_size, 50, screen_height - random_pipe_height - gap_size)
            pipes.append(top_pipe)
            pipes.append(bottom_pipe)

    if game_active:
        bird_velocity += bird_gravity
        bird_rect.centery += bird_velocity

        game_active = check_collision(pipes)
        if not game_active:
            game_over = True

        for pipe in pipes:
            pipe.centerx -= 5

        # Score when bird passes pipe
        for pipe in pipes:
            if pipe.centerx == bird_rect.centerx:
                score += 1
                if score > high_score:
                    high_score = score
                    save_high_score()

        # Remove off-screen pipes
        for pipe in pipes[:]:
            if pipe.right < 0:
                pipes.remove(pipe)

        pipes = [pipe for pipe in pipes if pipe.right > 0]

    if game_over:
        # Fade to black
        fade_alpha = min(255, fade_alpha + fade_speed)
        
        # Create fade surface
        fade_surface = pygame.Surface((screen_width, screen_height))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)
        screen.blit(fade_surface, (0, 0))
        
        # Fade in text after background fades
        if fade_alpha > 150:
            text_alpha = min(255, text_alpha + fade_speed)
            
            # Create text with alpha
            game_over_text = font.render("YOU DIED", True, (180, 0, 0))
            game_over_text.set_alpha(text_alpha)
            
            # Center text like Dark Souls
            text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
            
            screen.blit(game_over_text, text_rect)
    else:
        fade_alpha = max(0, fade_alpha - fade_speed)
        text_alpha = max(0, text_alpha - fade_speed)
        
        if fade_alpha > 0:
            fade_surface = pygame.Surface((screen_width, screen_height))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            screen.blit(fade_surface, (0, 0))
        
        screen.fill(bg)
        draw_bird()
        draw_pipes(pipes)
        
        # Draw score
        score_text = small_font.render(f"Score: {score}", True, (0, 0, 0))
        high_score_text = small_font.render(f"Best: {high_score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(high_score_text, (10, 40))
    pygame.display.update()
    clock.tick(60)
pygame.quit()