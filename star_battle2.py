# Example file showing a circle moving on screen
import copy
import random
import pygame


class Ship():
    def __init__(self, screen) -> None:
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 1.2)
        self.speed = 8
        self.color = "red"
        self.width = 100
        self.height = 30
        self.rect = self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
    
    def move_left(self):
        self.position.x -= self.speed

    def move_right(self):
        self.position.x += self.speed

    def draw(self, screen):
        x0 = self.position.x - self.width/2
        x1 = self.position.x + self.width/2
        y0 = self.position.y - self.height/2
        y1 = self.position.y + self.height/2
        self.rect = pygame.Rect( x0,y1, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect)
        # pygame.draw.circle(screen, self.color, self.position, 40)

    def get_position(self):
        return self.position

class Asteroid():
    def __init__(self, screen) -> None:
        self.position = pygame.Vector2(random.randint(0, screen.get_width()), 0)
        self.speed = random.randint(2, 8)
        self.color = "blue"
        self.radius = random.randint(30, 60)
        self.rect = pygame.Rect(self.position.x-self.radius/2, self.position.y-self.radius/2, self.radius, self.radius)
    
    def move(self):
        self.position.y += self.speed
        self.rect = pygame.Rect(self.position.x-self.radius/2, self.position.y-self.radius/2, self.radius, self.radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

    def get_rect(self):
        return self.rect

class Lazer:
    def __init__(self, point) -> None:
        self.position = copy.deepcopy(point) #pygame.Vector2(random.randint(0, screen.get_width()), 0)
        self.speed = 20
        self.color = "green"
        self.width = 10
        self.height = 30
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
    
    def move(self):
        self.position.y -= self.speed

    def draw(self, screen):
        self.rect = pygame.Rect(self.position.x, self.position.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, self.rect)

    def get_rect(self):
        return self.rect

class World:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.timer = 0
        self.ship = Ship(self.screen)
        self.asteroid_list = []
        self.lazers_list = []
        self.lazer_timer = 0
        self.lazer_fire_speed = 0.1

    def get_timer(self):
        return self.timer
    
    def time_to_spawn_asteroid(self):
        return self.time_to_spawn_asteroid

    def update_timer(self, dt):
        self.timer += dt
        if self.timer > 1:
            self.asteroid_list.append(Asteroid(self.screen))
            self.timer = 0
        if self.lazer_timer > 0:
            self.lazer_timer -= dt

    def get_ship(self):
        return self.ship
    
    def get_asteroids(self):
        return self.asteroid_list
    
    def get_lazers(self):
        return self.lazers_list
    
    def spawn_lazer(self):
        if self.lazer_timer <= 0:
            self.lazers_list.append(Lazer(self.ship.position))
            self.lazer_timer = self.lazer_fire_speed

class HandOfGod():
    
    def __init__(self, screen) -> None:
        self.screen = screen
        self.heigh_for_asteroids = 1000
       
    def handle_ship(self, world: World):
        keys = pygame.key.get_pressed()
        ship = world.get_ship()
        if keys[pygame.K_a]:
            ship.move_left()
        
        if keys[pygame.K_d]:
            ship.move_right()
        
        if keys[pygame.K_SPACE]:
            world.spawn_lazer()
    
    def handle_asteroids(self, world: World):
        asteroids = world.get_asteroids()
        for a in asteroids:
            a.move()

    def handle_lazers(self, world: World):
        asteroids = world.get_lazers()
        for a in asteroids:
            a.move()

    def clean_world(self, world):
        asteroids = world.get_asteroids()
        a_to_delete = []
        for a in asteroids:
            if a.position.y > self.heigh_for_asteroids:
                a_to_delete.append(a)
        for a in a_to_delete:
            asteroids.remove(a)

    def check_collisions(self, world:World):
        asteroids = world.get_asteroids()
        lazers = world.get_lazers()
        a_to_del = []
        l_to_del = []

        for a in asteroids:
            ar = a.get_rect()
            for l in lazers:
                lr = l.get_rect()
                collides = ar.colliderect(lr)
                if collides:
                    a_to_del.append(a)
                    l_to_del.append(l)
        
        for a in a_to_del:
            if a in asteroids:
                asteroids.remove(a)
        
        for l in l_to_del:
            if l in lazers:
                lazers.remove(l)


    def update_world(self, world:World):
        self.handle_ship(world)
        self.handle_lazers(world)
        self.handle_asteroids(world)
        self.clean_world(world)
        self.check_collisions(world)
        
    

class Drawer():
    def __init__(self, screen) -> None:
        self.screen = screen
        self.background_color = "black"
        self.obj_list = []

    def add_obj(self, obj):
        self.obj_list.append(obj)
    
    def draw(self, world:World):
        self.screen.fill(self.background_color)
        world.get_ship().draw(self.screen)
        for obj in world.get_asteroids():
            obj.draw(self.screen)

        for obj in world.get_lazers():
            obj.draw(self.screen)
        pygame.display.flip()



def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True

    hog = HandOfGod(screen)
    drawer = Drawer(screen)
    world = World(screen)

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        hog.update_world(world)
        drawer.draw(world)
        dt = clock.tick(60) / 1000
        world.update_timer(dt)

    pygame.quit()


if __name__ == "__main__":
    main()