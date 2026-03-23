import time
from src.npc import NPC
from src.player import Player
from src.rps import get_winner, CHOICES
from src.skill import BASIC_ATTACK

def combat_encounter(player: Player, enemy: NPC):
    print(f"\n--- COMBAT START: {player.name} vs {enemy.name} ---")
    
    while player.is_alive() and enemy.is_alive():
        print(f"\n[ {player.name} HP: {player.hp}/{player.max_hp} | {enemy.name} HP: {enemy.hp}/{enemy.max_hp} ]")
        
        # RPS Phase
        print("\n--- Rock - Paper - Scissors Phase ---")
        player_choice = ""
        while player_choice not in CHOICES:
            player_choice = input("Choose (rock/paper/scissors): ").lower().strip()
        
        enemy_choice = enemy.choose_rps()
        print(f"{enemy.name} chose: {enemy_choice}")
        
        winner = get_winner(player_choice, enemy_choice)
        
        # Reset buffs from previous round
        player.reset_buffs()
        enemy.reset_buffs()
        
        if winner == 1:
            print(">>> You won RPS! You attack first and gain +50% attack buff. <<<")
            player.attack += int(player.base_attack * 0.5)
            first_attacker, second_attacker = player, enemy
        elif winner == 2:
            print(f">>> {enemy.name} won RPS! They attack first and gain +50% attack buff. <<<")
            enemy.attack += int(enemy.base_attack * 0.5)
            first_attacker, second_attacker = enemy, player
        else:
            print(">>> It's a tie! No buffs, standard initiative (Player first). <<<")
            first_attacker, second_attacker = player, enemy
        
        # Combat Phase
        execute_turn(first_attacker, second_attacker)
        if second_attacker.is_alive():
            execute_turn(second_attacker, first_attacker)
            
    if player.is_alive():
        print(f"\n*** You defeated {enemy.name}! ***")
        return True
    else:
        print("\n*** You have been defeated... ***")
        return False

def execute_turn(attacker, defender):
    skill_used = None
    if hasattr(attacker, 'choose_skill'):
        # NPC Turn
        skill_used = attacker.choose_skill()
    else:
        # Player Turn
        print(f"\n{attacker.name}'s turn!")
        if not attacker.skills:
            skill_used = BASIC_ATTACK
        else:
            print("Available Skills:")
            for i, skill in enumerate(attacker.skills):
                print(f"{i+1}. {skill.name} (Power: {skill.power})")
            choice = -1
            while choice < 1 or choice > len(attacker.skills):
                try:
                    choice = int(input("Choose a skill number: "))
                except ValueError:
                    pass
            skill_used = attacker.skills[choice-1]
    
    if not skill_used:
        skill_used = BASIC_ATTACK

    damage_dealt = max(1, int((attacker.attack / 10) * skill_used.power))
    actual_damage = defender.take_damage(damage_dealt)
    
    print(f"> {attacker.name} uses {skill_used.name}!")
    print(f"> {defender.name} takes {actual_damage} damage!")
    time.sleep(1)   