class Player:
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.base_attack = attack
        self.attack = attack
        self.defense = defense
        self.skills = []

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, amount):
        damage = max(1, amount - self.defense)
        self.hp -= damage
        return damage

    def heal(self, amount):
        self.hp = min(self.max_hp, self.hp + amount)

    def add_skill(self, skill):
        self.skills.append(skill)

    def reset_buffs(self):
        self.attack = self.base_attack