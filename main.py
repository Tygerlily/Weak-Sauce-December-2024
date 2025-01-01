import random
import os


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
        self.level = level  # Use the level parameter instead of party_level

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
    # Check if the boss (Earthly God) has 50 hp
    for monster in monsters:
        if monster.name == "Earthly God" and (monster.hp <= 50 or player.hp <= 20):
            print(f"{Colors.RED}The Earthly God sways forward, moving it's body strangely. Once it stops swaying, it launches a sweeping attack!{Colors.RESET}")
            print(f"{Colors.RED}All the party members get forced away from you!{Colors.RESET}")
            return True  # Trigger forced en
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
        xp_gain = sum(monster.xp_reward for monster in monsters)
        Character.party_xp += xp_gain
        print(f"{Colors.GREEN}Victory! The party gained {xp_gain} XP!{Colors.RESET}")

        # Check if the party should level up
        while Character.party_xp >= Character.party_xp_to_level:
            Character.party_xp -= Character.party_xp_to_level
            Character.party_level += 1
            Character.party_xp_to_level = int(Character.party_xp_to_level * 1.5)  # Increase XP needed for next level
            print(f"{Colors.GREEN}The party leveled up to level {Character.party_level}!{Colors.RESET}")

            # Boost stats for all members
            for member in [player] + party:
                member.max_hp += 10
                member.hp = member.max_hp
                member.attack += 2
                member.magic += 1
                print(f"{member.name} powered up with the party level up!")

            print(f"{Colors.GREEN}The party has made it to their destination!{Colors.RESET}")
            return True

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

    print(f"{Colors.CYAN}Knight Rowen - Good luck, child{Colors.RESET}")
    input("")
    print(f"{Colors.RED}Blaze - Haha, yeah, we might need it{Colors.RESET}")
    input("")
    print(f"{Colors.YELLOW}Flip - As long as we don't die it'll be fine!{Colors.RESET}")
    input("")
    print(f"Knight Rowen smiles awkerdly at Flip")
    input("")

 

    print("You need to set out and fight your way to the border of the kingdom!")
    input("")

    # way to the border 1-2
    level = 1
    while level < 2:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()

    print("You've made it to the border of the Kingdom, you need to make your way to the cursed castle now")
    input("")
    print(f"{Colors.RED}Blaze - Why are the rats so large here? *shudders*{Colors.RESET}")
    input("")
    print(f"{Colors.YELLOW}Flip - Aww, Blaze! They're kinda cute in an ugly way! Like you!{Colors.RESET}")
    input("")
    print(f"{Colors.RED}Blaze - ... No comment ...{Colors.RESET}")
    input("")
    print("Fight your way to the cursed castle!")
    input("")
    #way to the castle 2-3
    while level < 3:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()



    # Cursed castle and character choice
    print("You arrive at the cursed castle and meet Knight Rowan. You know him well. He tells you that he's got to scout the area and can't come with you into the castle")
    input("")
    print(f"{Colors.CYAN}Knight Rowen - Looks like you lived! I'll be out here once you're done inside{Colors.RESET}")
    input("")
    print(f"{Colors.RED}Blaze - We could wait for you to finish before going in?{Colors.RESET}")
    input("")
    print(f"{Colors.YELLOW}Flip - Yeah! and go together, like a family!{Colors.RESET}")
    input("")
    print(f"{Colors.CYAN}Knight Rowen - HAHA, sure we can be a family, I'm still not helping you yet!{Colors.RESET}")
    input("")
    print("Fight your way to the throne room!")
    input("")

    while level < 4:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()

    #
    print("You come into the throne room, the sight of the evil King Malice stands before you")
    input("")
    print(f"{Colors.CYAN}King Malice - I don't want to fight you ... you don't know why you're here{Colors.RESET}")
    input("")
    print(f"{Colors.RED}Blaze - Uh... for like a heart thing{Colors.RESET}")
    input("")
    print(f"{Colors.CYAN}King Malice - *sigh* I do not have it. I never had{Colors.RESET}")
    input("")
    print(f"{Colors.YELLOW}Flip - We were told to come here?{Colors.RESET}")
    input("")
    print(f"{Colors.CYAN}King Malice - It's not like that at all. If you leave this place I'll die anyways, so I don't have what youre looking for or what you want{Colors.RESET}")
    input("")
    print(f"{Colors.CYAN}King Malice - The heart of a god should be with the god, no? Set me free and I'll come with you, leave me here and I'll die{Colors.RESET}")
    input("")
    print(f"{Colors.YELLOW}Flip - You are like an evil king...{Colors.RESET}")
    input("")
    print(f"{Colors.CYAN}King Malice - What???{Colors.RESET}")
    input("")
    print(f"{Colors.RED}Blaze - Yeah, for like 100's of years, you stole the heart{Colors.RESET}")
    input("")
    print(f"{Colors.CYAN}King Malice - Well, I didn't. All i know is that the rulers of your kingdom and I used to work together, we were going to harness the energy of the earthly god to bring peace. I foolishly thought that it meant that we would use the ambient energy that the god generates. However, the rulers of your kingdom wanted to harvest the heart. If its not in your kingdom then it's still in the god, I'll travel with you to simply look, but I will not harvest the heart with you.{Colors.RESET}")
    input("")
    print(f"{Colors.YELLOW}Flip - Why should we belive you?{Colors.RESET}")
    input("")
    print("King Malice tilts his head to the side, rasing his finger to point at you.")
    input("")
    print(f"{Colors.CYAN}King Malice - You are ... not a real person, simply a golemn, as I am. Perhaps you have cultivated a soul from ambient energy like I have. That is why I can tell you have earth magic, but my soul was cultivated with ice magic. I see you in myself{Colors.RESET}")

    partychoice = input("Choose your ally - King Malice (m) or Knight Rowan (r): ").lower()
    while partychoice not in ['m', 'r']:
        partychoice = input("Invalid choice. Choose your ally - King Malice (m) or Knight Rowan (r): ").lower()

    if partychoice == 'm':
        king_malice = Character("King Malice", 65, 15, 12)
        party.append(king_malice)
        print(f"{Colors.GREEN}King Malice joins your party!{Colors.RESET}")
        input("")
        print(f"{Colors.CYAN}King Malice - We need to leave through the secret passage if the knight is patrolling{Colors.RESET}")
        input("")
    elif partychoice == 'r':
        print(f"{Colors.CYAN}King Malice - I see you have decided to kill me. I do not blame you, I wouldn't trust me either{Colors.RESET}")
        input("")
        print(f"You leave the throne room and make your way out of the castle to meet up with Knight Rowen")
        input("")
        print(f"{Colors.CYAN}Knight Rowen - Looks like you made it back safe, the king should be dead in a fortnight, the seals in the walls of the castle will see to it.{Colors.RESET}")
        input("")
        knight_rowan = Character("Knight Rowan", 120, 20, 10)
        party.append(knight_rowan)
        print(f"{Colors.GREEN}Knight Rowan joins your party!{Colors.RESET}")
        input("")

    print("You're leaving the cursed castle now, fight your way to where the Earthly God is")
    input("")

    while level < 5:
        print(f"\nCurrent Party Level : {level}")
        num_monsters = random.randint(1, 4)
        enemies = generate_monsters(monsters[:level], num_monsters)
        if combat(player, party, enemies):
            level += 1
            player.level_up()

    print("You've made it to a clearing where there is a statue, the statue gets up... and now you need to fight!")
    input("")

    # Boss battle

    if partychoice == 'm':
        print(f"{Colors.CYAN}King Malice - Something is wrong! Look at its chest! The heart is missing! We've been tricked!{Colors.RESET}")
        input("")
        print(f"{Colors.RED}Blaze - Didn't your parents tell us to do this! They're the ones who set us up!{Colors.RESET}")
        input("")
        print(f"{Colors.YELLOW}Flip - Wait! are we the bad guys if we're doing this?{Colors.RESET}")
        input("")
        print(f"{Colors.CYAN}King Malice - There's no time! It's going to attack!{Colors.RESET}")
        input("")

        print("\nFinal Boss Battle!")
        boss = Monster("Earthly God", 160, 17, 0)
        combat(player, party, [boss])

        print(f"{Colors.RED}\nWAIT! THIS ISNT A VICTORY???\nThe Earthly God sways forward, moving it's body strangely. Once it stops swaying, it launches a sweeping attack!{Colors.RESET}")
        input("")
        print(f"{Colors.RED}All the party members get forced away from you!{Colors.RESET}")
        input("")
        print(f"{Colors.RED}The Earthly God dealt 100 damage to the party! Blaze, Flip, and King Malice are barely holding on, you're in too much pain to even move!{Colors.RESET}")
        input("")

        print("The Earthly God comes closer, reaches down, and grasps you in their hand.")
        input("")
        print("Blaze, Flip, and King Malice look upon you in horror, as the Earthly God crushes you in their palm. The Earthly God moves the meat that you have become into the cavity of their chest, there is a loud resonant hum and the Earthly God returns to what legends have foretold as the true power of the God.")
        input("")
        print("King Malice in fear of its power constructs a wall of ice to protect himself and the other party members if at all possible. Flip is desperately trying to heal King Malice and Blaze, so they have a chance to escape for survival. Blaze loses control of his demonic side slipping into baser instincts, his nails turning into proper claws, his horns, and his body growing in size, his skin ripping to meet the demands of his new form. Blaze gets up from his transformation and dashes forward to Flip and King Malice, roughly grabbing them, unfolding his wings into their full size, and he takes off for safety, leaving what is left of you behind.")
        input("")

    elif partychoice == 'r':
        print(f"{Colors.CYAN}Knight Rowan - Are you with me and with the Kingdom?{Colors.RESET}")
        choice = input (" (y) Yes (w) What (n) No : ")
        if choice == 'y':
            print("Knight Rowan smiles at you. A true, honest smile")
            input("")
            print(f"{Colors.CYAN}Knight Rowan - return to your place as the Heart. It calls to you, does it not? Your parents  need the Gods again, so you'll go back to being that. It is an honor how long your parents spent making you perfect, over and over, prince after princess, lord after lady, eldest son, eldest daughter, eldest child. How many lives have you lived in a humanoid form, I truly wonder! Return to your earthly god, child, and become what you once were!{Colors.RESET}")
            input("")
            print("You walk forward to the Earthly God, and as they get close, the Earthly God reaches down, and grasps you in their hand. Blaze and Flip look upon you in horror, while Knight Rowan starts to laugh joyously as the Earthly God crushes you in their palm. The Earthly God moves the heart that you have become into the cavity of their chest, there is a loud resonant hum and the Earthly God returns to what legends have foretold as the true power of the God. Flip is desperately trying to heal Blaze, so they have a chance to escape for survival. Blaze loses control of his demonic side slipping into baser instincts, his nails turning into proper claws, his horns, and his body growing in size, his skin ripping to meet the demands of his new form. Blaze gets up from his transformation and dashes forward to Flip roughly grabbing her, unfolding his wings into their full size, and he takes off for safety, leaving a smiling knight rowan and the Earthly God behind.")
            input("")
        if choice == ('w' or 'n') :
            print("Knight Rowan frowns at you, beyond disapointed")
            input("")
            print(f"{Colors.CYAN}why cant you just do what you are made for and follow directions you need to show penance before your maker, and return to your place as the Heart. Your parents need the Gods again, and no longer need a little royal subject for their plans. It is a shame that they spent so long trying to get you perfect, always failing, over and over, prince after princess, lord after lady, eldest son, eldest daughter, eldest child. How many lives have you lived missing what you were, return to your earthly god, child, there is no kingdom for you to come home to{Colors.RESET}")
            input("")
            print("Knight Rowan has left the party, and joined the Earthly God!")
            input("")
            print("\nFinal Boss Battle!")
            boss = Monster("Earthly God", 160, 17, 0)
            combat(player, party, [boss])
            print(f"{Colors.RED}\nWAIT! THIS ISNT A VICTORY???\nThe Earthly God sways forward, moving it's body strangely. Once it stops swaying, it launches a sweeping attack!{Colors.RESET}") 
            input("")
            print(f"{Colors.RED}All the party members get forced away from you!{Colors.RESET}")
            input("")
            print(f"{Colors.CYAN}Knight Rowan - Enough of this foolish game!{Colors.RESET}")
            input("")
            print("The Earthly God comes closer, reaches down, and grasps you in their hand.")
            input("")
            print("Blaze and Flip look upon you in horror, while Knight Rowan starts to laugh joyously  as the Earthly God crushes you in their palm. The Earthly God moves the meat that you have become into the cavity of their chest, there is a loud resonant hum and the Earthly God returns to what legends have foretold as the true power of the God.")
            input("")

    print("\n...\n...\n...Thanks for playing!")
    input("")

if __name__ == "__main__":
    main()
