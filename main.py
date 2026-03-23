import random
from src.player import Player
from src.npc import NPC
from src.combat import combat_encounter
from src.skill import BASIC_ATTACK, HEAVY_ATTACK, Skill

def generate_enemy(level):
    names = ["Goblin", "Orc", "Skeleton", "Troll", "Dark Knight"]
    name = random.choice(names)
    hp = 20 + (level * 10)
    attack = 5 + (level * 2)
    defense = 1 + level
    enemy = NPC(f"{name} Lvl {level}", hp, attack, defense)
    enemy.add_skill(BASIC_ATTACK)
    if level > 2:
        enemy.add_skill(HEAVY_ATTACK)
    return enemy

def main():
    print("====================================")
    print("  RPS ROGUELIKE: ROCK PAPER SLASH   ")
    print("====================================")
    
    player_name = input("Enter your hero's name: ")
    player = Player(player_name, hp=100, attack=10, defense=2)
    player.add_skill(BASIC_ATTACK)
    
    level = 1
    while player.is_alive():
        print(f"\n--- Floor {level} ---")
        enemy = generate_enemy(level)
        
        won = combat_encounter(player, enemy)
        if won:
            level += 1
            print("\n[ Level Up! ] Choose a reward:")
            print("1. Heal 40 HP")
            print("2. Increase Base Attack by +3")
            print("3. Learn 'Heavy Blow' Skill")
            
            choice = ""
            while choice not in ['1', '2', '3']:
                choice = input("Choice (1/2/3): ")
            
            if choice == '1':
                player.heal(40)
            elif choice == '2':
                player.base_attack += 3
            elif choice == '3':
                if HEAVY_ATTACK not in player.skills:
                    player.add_skill(HEAVY_ATTACK)
                else:
                    print("You already know this! Healed 20 HP instead.")
                    player.heal(20)
        else:
            print(f"\nGame Over! You reached Floor {level}.")
            break

if __name__ == "__main__":
    main()