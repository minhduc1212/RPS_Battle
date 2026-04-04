import time
import os
from src.npc import NPC
from src.player import Player
from src.rps import get_winner, CHOICES
from src.skill import BASIC_ATTACK

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_ui(player: Player, enemy: NPC, message: str = ""):
    clear_screen()
    print("=" * 70)
    print(f"{'RPS ROGUELIKE: COMBAT':^70}")
    print("=" * 70)
    print()
    
    player_sprite = [
        "                  _   ",
        "                 /-|  ",
        "               ___  \\ ",
        "______________|  /|--]",
        "              | / |__|",
        "               \\ /.\\ |",
        "                '|| ||",
        "                <_'<_'"
    ]
    
    enemy_sprite = [
        "      __,='`````'=/__ ",
        "     '//  >o< _ >o<  `'",
        "     //|      _      (`\\",
        "   ,-~~~\\   \\___/   /-,",
        "  /        `-----'     \\",
        " /      \\           /   \\",
        " |       '---------'    |",
        "  \\                    /"
    ]
    
    print(f"  {player.name:<30} {enemy.name:>30}")
    for p_line, e_line in zip(player_sprite, enemy_sprite):
        print(f"  {p_line:<30} {e_line:>30}")
        
    print()
    print(f"  {f'HP: {player.hp}/{player.max_hp}':<30} {f'HP: {enemy.hp}/{enemy.max_hp}':>30}")
    print(f"  {f'Attack: {player.attack}':<30} {f'Attack: {enemy.attack}':>30}")
    print(f"  {f'Defense: {player.defense}':<30} {f'Defense: {enemy.defense}':>30}")
    print("=" * 70)
    if message:
        print(f"{message}")

def combat_encounter(player: Player, enemy: NPC):
    draw_ui(player, enemy, f"\n--- COMBAT START: {player.name} vs {enemy.name} ---")
    time.sleep(1.5)
    
    while player.is_alive() and enemy.is_alive():
        
        # RPS Phase
        msg = "\n--- Rock - Paper - Scissors Phase ---\n"
        draw_ui(player, enemy, msg)
        player_choice = ""
        while player_choice not in CHOICES:
            player_choice = input("Choose (rock/paper/scissors): ").lower().strip()
            if player_choice not in CHOICES:
                draw_ui(player, enemy, msg + "Invalid choice, please try again.\n")
        
        enemy_choice = enemy.choose_rps()
        msg = f"\n{enemy.name} chose: {enemy_choice}\n"
        draw_ui(player, enemy, msg)
        time.sleep(1)
        
        winner = get_winner(player_choice, enemy_choice)
        
        # Reset buffs from previous round
        player.reset_buffs()
        enemy.reset_buffs()
        
        if winner == 1:
            msg += ">>> You won RPS! You attack first and gain +50% attack buff. <<<"
            player.attack += int(player.base_attack * 0.5)
            first_attacker, second_attacker = player, enemy
        elif winner == 2:
            msg += f">>> {enemy.name} won RPS! They attack first and gain +50% attack buff. <<<"
            enemy.attack += int(enemy.base_attack * 0.5)
            first_attacker, second_attacker = enemy, player
        else:
            msg += ">>> It's a tie! No buffs, standard initiative (Player first). <<<"
            first_attacker, second_attacker = player, enemy
            
        draw_ui(player, enemy, msg)
        time.sleep(2)
        
        # Combat Phase
        execute_turn(first_attacker, second_attacker, player, enemy)
        if second_attacker.is_alive():
            execute_turn(second_attacker, first_attacker, player, enemy)
            
    if player.is_alive():
        draw_ui(player, enemy, f"\n*** You defeated {enemy.name}! ***")
        time.sleep(1.5)
        return True
    else:
        draw_ui(player, enemy, "\n*** You have been defeated... ***")
        time.sleep(1.5)
        return False

def execute_turn(attacker: Player | NPC, defender: Player | NPC, player_ref: Player, enemy_ref: NPC):
    skill_used = None   
    if hasattr(attacker, 'choose_skill'):
        # NPC Turn
        skill_used = attacker.choose_skill()
    else:
        # Player Turn
        msg = f"\n{attacker.name}'s turn!\nAvailable Skills:\n"
        if not attacker.skills:
            skill_used = BASIC_ATTACK
        else:
            for i, skill in enumerate(attacker.skills):
                msg += f"{i+1}. {skill.name} (Power: {skill.power})\n"
            draw_ui(player_ref, enemy_ref, msg)
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
    
    msg = f"\n> {attacker.name} uses {skill_used.name}!\n> {defender.name} takes {actual_damage} damage!"
    draw_ui(player_ref, enemy_ref, msg)
    time.sleep(1.5)