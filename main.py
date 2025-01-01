import random
import os
import time

# Title Screen
def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("+=========================================+")
    print("|       The Chronicles of Magic Gods 1    |")
    print("+=========================================+")
    print("|               Credits:                  |")
    print("| Game main content:  gloomdev            |")
    print("+=========================================+")
    input("Press any key to continue...")

# Character class
class Character:
    def __init__(self, name, hp, attack, magic, level=1):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.magic = magic
        self.level = level
        self.xp = 0

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.attack += 2
        print(f"{self.name} leveled up to level {self.level}!")

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
    def __init__(self, name, hp, damage, xp_reward):
        self.name = name
        self.hp = hp
        self.damage = damage
        self.xp_reward = xp_reward

    def is_alive(self):
        return self.hp > 0

# Combat function
def combat(player, party, monsters):
    print("\nBattle Start!")
    while any(monster.is_alive() for monster in monsters) and any(member.is_alive() for member in [player] + party):
        for member in [player] + party:
            if member.is_alive():
                monster = random.choice([m for m in monsters if m.is_alive()])
                print(f"\n{member.name}'s turn! ({member.hp}/{member.max_hp} HP)")
                print_monsters(monsters)
                action = input("Attack (a), Magic (m), Block (b), or Run (r): ").lower()
                while action not in ['a', 'm', 'b', 'r']:
                    action = input("Invalid choice. Attack (a), Magic (m), Block (b), or Run (r): ").lower()
                if action == 'a':
                    damage = random.randint(member.attack - 2, member.attack + 2)
                    monster.hp -= damage
                    print(f"{member.name} dealt {damage} damage to {monster.name}!")
                elif action == 'm':
                    if member.name in ["Flip", "King Malice"]:
                        member.magic_heal_party([player] + party)
                    elif member.name == "Knight Rowan":
                        damage = random.randint(member.magic - 3, member.magic + 3)
                        monster.hp -= damage
                        print(f"{member.name} used magic and dealt {damage} damage to {monster.name}!")
                        print("Knight Rowan's magic attack also damages the party!")
                        for ally in [player] + party:
                            if ally.is_alive():
                                ally.hp = max(0, ally.hp - 3)
                                print(f"{ally.name} took 3 damage from Knight Rowan's magic attack!")
                    else:
                        damage = random.randint(member.magic - 3, member.magic + 3)
                        monster.hp -= damage
                        print(f"{member.name} used magic and dealt {damage} damage to {monster.name}!")
                elif action == 'b':
                    print(f"{member.name} blocks and takes reduced damage next turn!")
                elif action == 'r':
                    print("You ran away!")
                    return False

        # Monsters attack
        for monster in monsters:
            if monster.is_alive():
                target = random.choice([member for member in [player] + party if member.is_alive()])
                target.hp -= monster.damage
                print(f"{monster.name} dealt {monster.damage} damage to {target.name}!")
                if target.hp <= 0:
                    print(f"{target.name} has fainted!")

    if all(not monster.is_alive() for monster in monsters):
        xp_gain = sum(monster.xp_reward for monster in monsters)
        print(f"Victory! Gained {xp_gain} XP.")
        player.xp += xp_gain
        for member in party:
            member.xp += xp_gain
            if member.xp >= member.level * 20:
                member.level_up()
        return True
    return False

# Display monsters
def print_monsters(monsters):
    print("Enemies:")
    for monster in monsters:
        print(f"{monster.name} - HP: {monster.hp}")

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

    # Starting Dialogue
    print("The King - My child has volunteered to bring peace back to our kingdom, by going to the cursed castle of the evil King Malice and taking back the heart of the Earthly God, and bringing it back where it rightly belongs.")
    input("")
    print("The Queen - Our brave child is going to be joined by two great warriors, The half-demon Blaze, and the fairy mage Flip.")
    input("")
    print("The King - Go forth my child, and bring us peace")
    input("")



    # Monsters
    monsters = [
        Monster("Large Rat", 10, 3, 5),
        Monster("Forest Spirit", 20, 6, 10),
        Monster("Centaur Statue", 30, 9, 15),
        Monster("Rock Golem", 40, 12, 20)
    ]

    print("Fight your way to the border of the kingdom")
    input("...")

    # way to the border 1-2
    level = 1
    while level < 2:
        print(f"\nLevel {level} begins!")
        num_monsters = random.randint(1, 4)
        enemies = random.choices(monsters[:level], k=num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()

    print("Fight your way to the cursed castle")
    input("...")
    #way to the castle 2-3
    while level < 3:
        print(f"\nLevel {level} begins!")
        num_monsters = random.randint(1, 4)
        enemies = random.choices(monsters[:level], k=num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()



    # Cursed castle and character choice
    print("You arrive at the cursed castle and meet Knight Rowan. You know him well. He tells you that he's got to scout the area and can't come with you")
    print("Fight your way to the throne room!")
    input("...")

    while level < 4:
        print(f"\nLevel {level} begins!")
        num_monsters = random.randint(1, 4)
        enemies = random.choices(monsters[:level], k=num_monsters)
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
        print("King Malice joins your party!")
    elif choice == 'r':
        knight_rowan = Character("Knight Rowan", 120, 20, 10)
        party.append(knight_rowan)
        print("Knight Rowan joins your party!")

    print("You're leaving the cursed castle now, fight your way to where the Earthly God is")
    input("...")

    while level < 4:
        print(f"\nLevel {level} begins!")
        num_monsters = random.randint(1, 4)
        enemies = random.choices(monsters[:level], k=num_monsters)
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
