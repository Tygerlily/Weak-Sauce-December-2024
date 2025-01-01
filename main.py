import random
import os
import time


# ANSI colors to help with reading and vibes
class Colors:
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


# Title Screen
def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("+=========================================+")
    print(f"|   {Colors.GREEN}The Chronicles of the Elemental Gods {Colors.RESET} |")
    print("+=========================================+")
    print("|               Credits:                  |")
    print("| Game main content:  gloomdev            |")
    print("+=========================================+")
    input("Press any key to continue...")

# Character class
class Character:

    party_level = 1
    party_xp = 0
    party_xp_to_level = 40

    def __init__(self, name, hp, attack, magic, level=1):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.magic = magic
        self.level = party_level

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 2
        print(f"{Colors.GREEN}{self.name} leveled up to level {self.level}!{Colors.RESET}")

    def is_alive(self):
        return self.hp > 0

    def heal(self):
        self.hp = self.max_hp

    def magic_heal_party(self, party):
        for member in party:
            if member.is_alive():
                heal_amount = random.randint(8, 15)
                member.hp = min(member.max_hp, member.hp + heal_amount)
                print(f"{self.name} healed {member.name} for {heal_amount} HP!")

# Monster class
class Monster:
    def __init__(self, base_name, hp, damage, xp_reward, number=1):
        self.base_name = base_name  # name
        self.name = f"{base_name} {number}"  # adding number
        self.hp = hp
        self.damage = damage
        self.xp_reward = xp_reward

    def is_alive(self):
        return self.hp > 0
    
def force_end_combat(player, monsters):
    # Check if the boss (Earthly God) has low HP
    for monster in monsters:
        if monster.name == "Earthly God" and monster.hp <= 90:
            print(f"{Colors.RED}The Earthly God is weakened and unable to continue!{Colors.RESET}")
            return True  # Trigger forced end

    # Check if the player is too weak to continue
    if player.hp <= 20:
        print(f"{Colors.RED}{player.name} is too weak to continue the battle!{Colors.RESET}")
        return True  # Trigger forced end
    
    return False

def combat(player, party, monsters):
    while any(monster.is_alive() for monster in monsters) and any(member.is_alive() for member in [player] + party):
        # Check before any player actions
        if force_end_combat(player, monsters):
            return True  # End combat immediately

        for member in [player] + party:
            if member.is_alive():
                alive_monsters = [m for m in monsters if m.is_alive()]
                if alive_monsters:
                    print(f"\n{member.name}'s turn! ({member.hp}/{member.max_hp} HP)")
                    print_monsters(monsters)

                    action = input("Attack (a), Magic (m), Block (b), or Run (r): ").lower()
                    while action not in ['a', 'm', 'b', 'r']:
                        action = input("Invalid choice. Attack (a), Magic (m), Block (b), or Run (r): ").lower()
                    
                    if action == 'a':
                        if len(alive_monsters) == 1:  # Only 1 enemy left
                            # Automatically target the only remaining enemy
                            monster = alive_monsters[0]
                            damage = random.randint(member.attack - 2, member.attack + 2)
                            monster.hp -= damage
                            print(f"{member.name} dealt {damage} damage to {monster.name}!")
                        else:
                            # Ask the player to select a target if more than 1 enemy
                            print_monsters(alive_monsters)
                            target_index = int(input("Choose target by number (1, 2, etc.): ")) - 1
                            if 0 <= target_index < len(alive_monsters):
                                monster = alive_monsters[target_index]
                                damage = random.randint(member.attack - 2, member.attack + 2)
                                monster.hp -= damage
                                print(f"{member.name} dealt {damage} damage to {monster.name}!")
                    elif action == 'm':
                        if member.name in ["Flip", "King Malice"]:  # Check if the character is Flip or King Malice
                            heal_amount = random.randint(8, 15)
                            for ally in [player] + party:  # Heal all party members
                                if ally.is_alive():
                                    ally.hp = min(ally.max_hp, ally.hp + heal_amount)  # Don't overheal
                                    print(f"{member.name} healed {ally.name} for {heal_amount} HP!")
                        else:  # Damage enemies if not Flip or malice
                            damage = random.randint(member.magic - 3, member.magic + 3)
                            for monster in alive_monsters:
                                monster.hp -= damage
                                print(f"{member.name} used magic and dealt {damage} damage to {monster.name}!")
                    elif action == 'b':
                        print(f"{member.name} blocks and takes reduced damage next turn!")
                    elif action == 'r':
                        print("You ran away!")
                        print("Running away makes you encounter more monsters!")
                        # Heal the party!!!! omg
                        player.heal()
                        for member in party:
                            member.heal()
                        print(f"{Colors.GREEN}The party's HP has been fully restored anyways!{Colors.RESET}")
                        return False

                    # Check after player's action
                    if force_end_combat(player, monsters):
                        return True  # End combat immediately

        # Monsters attack
        for monster in monsters:
            if monster.is_alive():
                target = random.choice([member for member in [player] + party if member.is_alive()])
                target.hp -= monster.damage
                print(f"{Colors.RED}{monster.name} dealt {monster.damage} damage to {target.name}!{Colors.RESET}")
                
                # Check after monster's attack
                if force_end_combat(player, monsters):
                    return True  # End combat immediately
                if target.hp <= 0:
                    print(f"{target.name} has fainted!")

    if all(not monster.is_alive() for monster in monsters):
        global party_xp, party_level, party_xp_to_level

        xp_gain = sum(monster.xp_reward for monster in monsters)
        party_xp += xp_gain
        print(f"{Colors.GREEN}Victory! The party gained {xp_gain} XP!{Colors.RESET}")

        # Check if the party should level up
        while party_xp >= party_xp_to_level:
            party_xp -= party_xp_to_level
            party_level += 1
            party_xp_to_level = int(party_xp_to_level * 1.5)  # Increase XP needed for next level
            print(f"{Colors.GREEN}The party leveled up to level {party_level}!{Colors.RESET}")

            # Boost stats for all members
            for member in [player] + party:
                member.max_hp += 10
                member.hp = member.max_hp
                member.attack += 2
                member.magic += 1
                print(f"{member.name} powered up with the party level up!")

# Display monsters
def print_monsters(monsters):
    print("Enemies:")
    for monster in monsters:
        color = Colors.RED if monster.hp > 0 else Colors.MAGENTA  # Red if alive, Green if dead
        print(f"{color}{monster.name} - HP: {monster.hp}{Colors.RESET}")


def generate_monsters(base_monsters, num_monsters):
    monster_counts = {}
    enemies = []
    for _ in range(num_monsters):
        base_monster = random.choice(base_monsters)
        # Track counts based on the base name
        base_name = base_monster.base_name
        monster_counts[base_name] = monster_counts.get(base_name, 0) + 1
        # Generate unique name
        enemies.append(Monster(
            base_name,
            base_monster.hp,
            base_monster.damage,
            base_monster.xp_reward,
            monster_counts[base_name]
        ))
    return enemies

# Main function
def main():
    title_screen()
    os.system('cls' if os.name == 'nt' else 'clear')

    # Create characters
    player_name = input("Enter your character's name: ")
    player = Character(player_name, 45, 10, 8)
    blaze = Character("Blaze", 50, 12, 10)
    flip = Character("Flip", 40, 9, 12)

    party = [blaze, flip]

    # Monsters health/hit/exp
    monsters = [
        Monster("Large Rat", 20, 3, 5),
        Monster("Forest Spirit", 30, 6, 10),
        Monster("Centaur Statue", 40, 9, 15),
        Monster("Rock Golem", 50, 12, 20)
    ]

    # Starting Dialogue
    print("The King - My child has volunteered to bring peace back to our kingdom, by going to the cursed castle of the evil King Malice and taking back the heart of the Earthly God, and bringing it back where it rightly belongs.")
    input("")
    print("The Queen - Our brave child is going to be joined by two great warriors, The half-demon Blaze, and the fairy mage Flip.")
    input("")
    print("The King - Go forth my child, and bring us peace")
    input("")



 

    print("Fight your way to the border of the kingdom")
    input("...")

    # way to the border 1-2
    level = 1
    while level < 2:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()

    print("Fight your way to the cursed castle")
    input("...")
    #way to the castle 2-3
    while level < 3:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()



    # Cursed castle and character choice
    print("You arrive at the cursed castle and meet Knight Rowan. You know him well. He tells you that he's got to scout the area and can't come with you")
    print("Fight your way to the throne room!")
    input("...")

    while level < 4:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()

    #
    print("Meet King Malice, he doesnt want to fight")
    choice = input("Choose your ally - King Malice (m) or Knight Rowan (r): ").lower()
    while choice not in ['m', 'r']:
        choice = input("Invalid choice. Choose your ally - King Malice (m) or Knight Rowan (r): ").lower()

    if choice == 'm':
        king_malice = Character("King Malice", 65, 15, 12)
        party.append(king_malice)
        print(f"{Colors.CYAN}King Malice joins your party!{Colors.RESET}")
    elif choice == 'r':
        knight_rowan = Character("Knight Rowan", 120, 20, 10)
        party.append(knight_rowan)
        print(f"{Colors.CYAN}Knight Rowan joins your party!{Colors.RESET}")

    print("You're leaving the cursed castle now, fight your way to where the Earthly God is")
    input("...")

    while level < 4:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()

    print("You've made it to a clearing where there is a statue, the statue gets up... and now you need to fight!")
    input("...")

    # Boss battle
    print("\nFinal Boss Battle!")
    boss = Monster("Earthly God", 160, 16, 0)
    combat(player, party, [boss])

    print("Thanks for playing!")
    input("...")

if __name__ == "__main__":
    main()
