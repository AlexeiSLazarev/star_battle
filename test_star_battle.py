import unittest
from star_battle import Game, Player, Obstacle

class TestPlayer(unittest.TestCase):
    def test_player_movement(self):
        player = Player(100, 100)
        player.move(10, 0)
        self.assertEqual(player.rect.x, 110)
        player.move(-20, 0)
        self.assertEqual(player.rect.x, 90)

    def test_player_boundaries(self):
        player = Player(0, 0)
        player.move(-10, 0)
        self.assertEqual(player.rect.x, 0)  # Не выходит за границу
        player.move(900, 0)
        self.assertEqual(player.rect.x, 750)  # Максимальная позиция

class TestObstacle(unittest.TestCase):
    def test_obstacle_movement(self):
        obstacle = Obstacle(100, 100)
        obstacle.update()
        self.assertEqual(obstacle.rect.y, 100 + 5)

    def test_obstacle_off_screen(self):
        obstacle = Obstacle(100, 601)
        self.assertTrue(obstacle.is_off_screen())
        obstacle = Obstacle(100, 599)
        self.assertFalse(obstacle.is_off_screen())

class TestGame(unittest.TestCase):
    def test_spawn_obstacle(self):
        game = Game()
        self.assertEqual(len(game.obstacles), 0)
        game.spawn_obstacle()
        self.assertEqual(len(game.obstacles), 1)

    def test_game_updates_score(self):
        game = Game()
        game.spawn_obstacle()
        obstacle = game.obstacles[0]
        obstacle.rect.y = 601  # За экраном
        game.update()
        self.assertEqual(game.score, 1)

    def test_game_over_on_collision(self):
        game = Game()
        game.spawn_obstacle()
        obstacle = game.obstacles[0]
        obstacle.rect.y = game.player.rect.y
        obstacle.rect.x = game.player.rect.x
        game.update()
        self.assertFalse(game.running)

if __name__ == "__main__":
    unittest.main()
