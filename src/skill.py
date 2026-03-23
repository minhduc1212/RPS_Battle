class Skill:
    def __init__(self, name, power, description):
        self.name = name
        self.power = power
        self.description = description

BASIC_ATTACK = Skill("Strike", 10, "A basic melee attack.")
HEAVY_ATTACK = Skill("Heavy Blow", 20, "A slow but powerful attack.")