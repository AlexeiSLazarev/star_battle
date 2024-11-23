
import unittest
import pygame
from star_battle2 import World, Ship, Asteroid, Lazer, HandOfGod

class TestLogicalLevel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))

    def test_ship_movement(self):
        ship = Ship(self.screen)
        initial_position = ship.position.x
        ship.move_left()
        self.assertLess(ship.position.x, initial_position, "Ship should move left.")
        ship.move_right()
        self.assertEqual(ship.position.x, initial_position, "Ship should return to initial position.")

    def test_asteroid_movement(self):
        asteroid = Asteroid(self.screen)
        initial_position = asteroid.position.y
        asteroid.move()
        self.assertGreater(asteroid.position.y, initial_position, "Asteroid should move down.")

    def test_lazer_movement(self):
        point = pygame.Vector2(100, 100)
        lazer = Lazer(point=point)
        initial_position = lazer.position.y
        lazer.move()
        self.assertLess(lazer.position.y, initial_position, "Lazer should move up.")

    def tearDown(self):
        pygame.quit()


class TestModularLevel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.world = World(self.screen)

    def test_spawn_asteroids(self):
        initial_count = len(self.world.get_asteroids())
        self.world.update_timer(1.1)  # Enough time to spawn an asteroid
        self.assertEqual(len(self.world.get_asteroids()), initial_count + 1, "Asteroid should spawn.")

    def test_spawn_lazer(self):
        initial_count = len(self.world.get_lazers())
        self.world.spawn_lazer()
        self.assertEqual(len(self.world.get_lazers()), initial_count + 1, "Lazer should spawn.")

    def test_clean_world(self):
        hog = HandOfGod(self.screen)
        asteroid = Asteroid(self.screen)
        asteroid.position.y = 1500  # Move asteroid out of bounds
        self.world.asteroid_list.append(asteroid)
        hog.clean_world(self.world)
        self.assertNotIn(asteroid, self.world.get_asteroids(), "Out-of-bounds asteroid should be removed.")

    def tearDown(self):
        pygame.quit()


class TestTraceLevel(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.world = World(self.screen)
        self.hog = HandOfGod(self.screen)

    def test_collision_handling(self):
        asteroid = Asteroid(self.screen)
        lazer = Lazer(point=asteroid.position)
        self.world.asteroid_list.append(asteroid)
        self.world.lazers_list.append(lazer)
        self.hog.check_collisions(self.world)
        self.assertNotIn(asteroid, self.world.get_asteroids(), "Asteroid should be removed after collision.")
        self.assertNotIn(lazer, self.world.get_lazers(), "Lazer should be removed after collision.")

    def test_timer_update(self):
        initial_timer = self.world.get_timer()
        self.world.update_timer(0.5)
        self.assertAlmostEqual(self.world.get_timer(), initial_timer + 0.5, places=2, msg="Timer should update correctly.")

    def tearDown(self):
        pygame.quit()


if __name__ == "__main__":
    unittest.main()
