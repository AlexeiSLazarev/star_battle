import random
import pygame


class GameObject:
    def __init__(self, position, speed, color, width, height):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)

    def move(self, dx=0, dy=0):
        self.position.x += dx * self.speed
        self.position.y += dy * self.speed
        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.position.x - self.width / 2,
                                self.position.y - self.height / 2,
                                self.width, self.height)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Ship(GameObject):
    def __init__(self, screen):
        super().__init__((screen.get_width() / 2, screen.get_height() / 1.2), 8, "red", 100, 30)

class Asteroid(GameObject):
    def __init__(self, screen):
        position = (random.randint(0, screen.get_width()), 0)
        speed = random.randint(2, 8)
        radius = random.randint(30, 60)
        super().__init__(position, speed, "blue", radius, radius)

    def move(self):
        super().move(dy=1)

class Lazer(GameObject):
    def __init__(self, position):
        super().__init__(position, 20, "green", 10, 30)

    def move(self):
        super().move(dy=-1)


class HandOfGod:
    def handle_input(self, ship, keys, world):
        if keys[pygame.K_a]: 
            ship.move(dx=-1)
        if keys[pygame.K_d]:
            ship.move(dx=1)
        if keys[pygame.K_SPACE]: 
            world.spawn_lazer(ship.position)

    def update(self, world, dt):
        world.update_timer(dt)
        for asteroid in world.get_asteroids():
            asteroid.move()
        for lazer in world.get_lazers():
            lazer.move()
        world.check_collisions()


class World:
    def __init__(self, screen):
        self.screen = screen
        self.timer = 0
        self.ship = Ship(screen)
        self.asteroid_list = []
        self.lazer_list = []
        self.lazer_cooldown = 0.1
        self.lazer_timer = 0

    def update_timer(self, dt):
        self.timer += dt
        self.lazer_timer -= dt
        if self.timer > 1:
            self.asteroid_list.append(Asteroid(self.screen))
            self.timer = 0

    def spawn_lazer(self, position):
        if self.lazer_timer <= 0:
            self.lazer_list.append(Lazer(position))
            self.lazer_timer = self.lazer_cooldown

    def get_ship(self):
        return self.ship

    def get_asteroids(self):
        return self.asteroid_list

    def get_lazers(self):
        return self.lazer_list

    def check_collisions(self):
        to_remove_asteroids = []
        to_remove_lazers = []
        for asteroid in self.asteroid_list:
            for lazer in self.lazer_list:
                if asteroid.rect.colliderect(lazer.rect):
                    to_remove_asteroids.append(asteroid)
                    to_remove_lazers.append(lazer)

        for asteroid in to_remove_asteroids:
            if asteroid in self.asteroid_list:
                self.asteroid_list.remove(asteroid)

        for lazer in to_remove_lazers:
            if lazer in self.lazer_list:
                self.lazer_list.remove(lazer)


class Drawer:
    def __init__(self, screen):
        self.screen = screen
        self.background_color = "black"

    def draw(self, world: World):

        self.screen.fill(self.background_color)

        world.get_ship().draw(self.screen)
        for asteroid in world.get_asteroids():
            asteroid.draw(self.screen)
        for lazer in world.get_lazers():
            lazer.draw(self.screen)

        pygame.display.flip()



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    world = World(screen)
    hand_of_god = HandOfGod()
    drawer = Drawer(screen)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        hand_of_god.handle_input(world.get_ship(), keys, world)
        dt = clock.tick(60) / 1000 
        hand_of_god.update(world, dt)

        drawer.draw(world)

    pygame.quit()


if __name__ == "__main__":
    main()