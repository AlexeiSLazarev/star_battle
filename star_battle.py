import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 20
OBSTACLE_SPEED = 5

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, self.rect.x))
        self.rect.y = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, self.rect.y))


class Obstacle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

    def update(self):
        self.rect.y += OBSTACLE_SPEED

    def is_off_screen(self):
        return self.rect.y > SCREEN_HEIGHT


class Game:
    def __init__(self):
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.obstacles = []
        self.score = 0
        self.running = True

    def spawn_obstacle(self):
        x = random.randint(0, SCREEN_WIDTH - OBSTACLE_WIDTH)
        self.obstacles.append(Obstacle(x, 0))

    def update(self):
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 1
            elif obstacle.rect.colliderect(self.player.rect):
                self.running = False

    def handle_input(self, keys):
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 5
        self.player.move(dx, dy)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Avoid the Obstacles")
    clock = pygame.time.Clock()
    game = Game()

    # Таймер для генерации препятствий
    obstacle_spawn_timer = 0
    obstacle_spawn_interval = 1000  # Интервал появления препятствий (мс)

    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False

        keys = pygame.key.get_pressed()
        game.handle_input(keys)

        # Таймер появления препятствий
        obstacle_spawn_timer += clock.get_time()
        if obstacle_spawn_timer >= obstacle_spawn_interval:
            game.spawn_obstacle()
            obstacle_spawn_timer = 0

        # Обновление игры
        game.update()

        # Рендеринг
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (0, 255, 0), game.player.rect)  # Игрок
        for obstacle in game.obstacles:
            pygame.draw.rect(screen, (255, 0, 0), obstacle.rect)  # Препятствия
        pygame.display.flip()

        clock.tick(30)  # Ограничение FPS

    pygame.quit()

if __name__ == "__main__":
    main()
