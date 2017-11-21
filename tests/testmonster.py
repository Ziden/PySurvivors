import unittest
from src.scenario import Scene
from src.monster import Zombie
import sys

class TestMonster(unittest.TestCase):

	scene = None

	def setUp(self):
		scene = Scene()

	def testHit(self):
		zombie = Zombie(self.scene, 0,0)

		# we got 1 zombie now
		assertEqual(len(scene.zombies), 1)

		damage = scene.getPlayer().gun.damage
		
		zombielife = zombie.hp

		numberOfHits = zombielife / damage
		print numberOfHits

unittest.main()

