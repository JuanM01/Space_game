import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Invasión Espacial")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, BLUE, [(0, 40), (25, 0), (50, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            return Bullet(self.rect.centerx, self.rect.top)
        return None

# Enemigos
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, RED, [(0, 0), (40, 20), (0, 40)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 3)

# Balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Power-ups
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = 2

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

# Funciones
def spawn_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def spawn_powerup():
    if random.random() < 0.01:  # 1% de probabilidad en cada frame
        powerup = PowerUp()
        all_sprites.add(powerup)
        powerups.add(powerup)

def show_menu():
    menu = True
    difficulty = 1
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True, difficulty
                elif event.key == pygame.K_UP:
                    difficulty = min(difficulty + 1, 3)
                elif event.key == pygame.K_DOWN:
                    difficulty = max(difficulty - 1, 1)

        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        title = font.render("Invasión Espacial", True, WHITE)
        instructions = font.render("Presiona ESPACIO para comenzar", True, WHITE)
        difficulty_text = font.render(f"Dificultad: {'Fácil' if difficulty == 1 else 'Normal' if difficulty == 2 else 'Difícil'}", True, WHITE)
        difficulty_instructions = font.render("Usa las flechas ARRIBA/ABAJO para cambiar la dificultad", True, WHITE)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT//2))
        screen.blit(difficulty_text, (WIDTH//2 - difficulty_text.get_width()//2, HEIGHT//2 + 50))
        screen.blit(difficulty_instructions, (WIDTH//2 - difficulty_instructions.get_width()//2, HEIGHT//2 + 100))
        
        pygame.display.flip()

    return False, 0

def game_over(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("¡Juego Terminado!", True, WHITE)
    score_text = font.render(f"Puntuación final: {score}", True, WHITE)
    restart_text = font.render("Presiona R para reiniciar", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
    return False

# Bucle principal del juego
def main():
    global player

    play, difficulty = show_menu()
    if not play:
        return

    # Crear enemigos iniciales
    for i in range(5 * difficulty):
        spawn_enemy()

    score = 0
    level = 1
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    bullet = player.shoot()
                    if bullet:
                        all_sprites.add(bullet)
                        bullets.add(bullet)

        # Actualizar
        all_sprites.update()

        # Colisiones jugador - enemigo
        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            if not game_over(score):
                return
            else:
                # Reiniciar el juego
                player.rect.centerx = WIDTH // 2
                player.rect.bottom = HEIGHT - 10
                all_sprites.empty()
                enemies.empty()
                bullets.empty()
                powerups.empty()
                all_sprites.add(player)
                for i in range(5 * difficulty):
                    spawn_enemy()
                score = 0
                level = 1

        # Colisiones balas - enemigos
        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 10
            spawn_enemy()

        # Colisiones jugador - power-ups
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            player.shoot_delay = max(player.shoot_delay - 50, 100)  # Aumenta la velocidad de disparo

        # Generar power-ups
        spawn_powerup()

        # Dibujar
        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Mostrar puntuación y nivel
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        level_text = font.render(f"Nivel: {level}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

        pygame.display.flip()

        # Aumentar la dificultad y subir de nivel
        if score > level * 100:
            level += 1
            for i in range(2):
                spawn_enemy()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

