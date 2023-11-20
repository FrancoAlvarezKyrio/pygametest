import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Shooter Game")

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Jugador
player_size = 50
player_x, player_y = width // 2 - player_size // 2, height - 2 * player_size
player_speed = 8

# Enemigos
enemy_size = 50
enemy_speed = 5
enemies = []

# Lista de disparos
bullets = []
bullet_speed = 10

# Estado del juego
game_active = False

# Puntuación
score = 0

# Fuente y tamaño del texto
font = pygame.font.Font(None, 36)

# Función para dibujar el jugador
def draw_player(x, y):
    pygame.draw.rect(screen, white, (x, y, player_size, player_size))

# Función para dibujar enemigos
def draw_enemies():
    for enemy in enemies:
        pygame.draw.rect(screen, red, (enemy[0], enemy[1], enemy_size, enemy_size))

# Función para dibujar disparos
def draw_bullets():
    for bullet in bullets:
        pygame.draw.rect(screen, white, (bullet[0], bullet[1], 5, 10))

# Función para manejar la lógica de los disparos
def handle_bullets():
    for bullet in bullets:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

# Función para manejar la lógica de los enemigos
def handle_enemies():
    global enemies, game_active, score

    for enemy in enemies:
        enemy[1] += enemy_speed
        if enemy[1] > height:
            enemies.remove(enemy)
            score += 1  # Incrementar la puntuación por cada cuadrado rojo que desaparece

        # Verificar colisiones entre jugador y enemigos
        if (
            player_x < enemy[0] + enemy_size
            and player_x + player_size > enemy[0]
            and player_y < enemy[1] + enemy_size
            and player_y + player_size > enemy[1]
        ):
            game_over()

# Función para detectar colisiones entre disparos y enemigos
def check_collisions():
    global enemies, bullets, score

    for bullet in bullets:
        for enemy in enemies:
            if (
                bullet[0] < enemy[0] + enemy_size
                and bullet[0] + 5 > enemy[0]
                and bullet[1] < enemy[1] + enemy_size
                and bullet[1] + 10 > enemy[1]
            ):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 10  # Incrementar la puntuación por cada cuadrado rojo alcanzado

# Función para mostrar el menú
def show_menu():
    screen.fill(black)
    text_play = font.render("1. Jugar", True, white)
    text_quit = font.render("2. Salir", True, white)
    text_instructions = font.render("3. Instrucciones", True, white)
    screen.blit(text_play, (width // 2 - text_play.get_width() // 2, height // 2 - 100))
    screen.blit(text_quit, (width // 2 - text_quit.get_width() // 2, height // 2 - 50))
    screen.blit(text_instructions, (width // 2 - text_instructions.get_width() // 2, height // 2))
    pygame.display.flip()

# Función para mostrar las instrucciones
def show_instructions():
    screen.fill(black)
    instructions_text = [
        "Instrucciones:",
        "Moverse hacia los costados con las flechas",
        "Disparar con la barra espaciadora",
        "",
        "Presiona 'ESC' para volver al menú",
    ]
    for i, line in enumerate(instructions_text):
        text = font.render(line, True, white)
        screen.blit(text, (width // 2 - text.get_width() // 2, 50 + i * 50))
    pygame.display.flip()
    wait_for_key()

# Función para mostrar la pantalla de Game Over
def game_over():
    global game_active, score

    game_active = False
    screen.fill(black)
    text_game_over = font.render("Game Over", True, white)
    text_score = font.render(f"Puntuación: {score}", True, white)
    screen.blit(text_game_over, (width // 2 - text_game_over.get_width() // 2, height // 2 - 50))
    screen.blit(text_score, (width // 2 - text_score.get_width() // 2, height // 2))
    pygame.display.flip()
    wait_for_key()

# Función para esperar a que se presione una tecla
def wait_for_key():
    global game_active, score, player_x, player_y, enemies, bullets

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    reset_game()
                    return
                waiting = False

# Función para reiniciar el juego
def reset_game():
    global game_active, score, player_x, player_y, enemies, bullets

    game_active = True
    score = 0
    player_x, player_y = width // 2 - player_size // 2, height - 2 * player_size
    enemies = []
    bullets = []

# Función principal del juego
def game():
    global player_x, player_y, game_active, bullets, score

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    reset_game()
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_3:
                    show_instructions()
                elif event.key == pygame.K_SPACE and game_active:
                    bullets.append([player_x + player_size // 2 - 2, player_y])

        if game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < width - player_size:
                player_x += player_speed

            # Generar enemigos aleatorios
            if random.randint(0, 100) < 5:
                enemy_x = random.randint(0, width - enemy_size)
                enemy_y = -enemy_size
                enemies.append([enemy_x, enemy_y])

            # Actualizar la pantalla
            screen.fill(black)
            draw_player(player_x, player_y)
            handle_enemies()
            draw_enemies()

            # Dibujar y manejar los disparos
            draw_bullets()
            handle_bullets()

            # Verificar colisiones entre disparos y enemigos
            check_collisions()
        else:
            show_menu()

        pygame.display.flip()

        # Establecer la velocidad del bucle
        clock.tick(30)

# Ejecutar el juego
game()
