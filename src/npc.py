import random
from src.player import Player

class NPC(Player):
    def __init__(self, name, hp, attack, defense):
        super().__init__(name, hp, attack, defense)

    def choose_rps(self):
        from src.rps import CHOICES
        return random.choice(CHOICES)

    def choose_skill(self):
        if not self.skills:
            return None
        return random.choice(self.skills)