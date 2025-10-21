import random

# Base Character Class
class Character():
    def __init__(self, name, health, attack_power):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.max_health = health

        # Defensive
        self.block_next = False  # Blocks next attack for no damage
        self.evade_next =False  # Evades next attack no damage
        self.guard_next =0.0  # Guards next attack for a percentage

        # Heals
        self.heal_uses = 3  # Amount that can be used
        self.heal_amount = 25  # Amount of health to be restored

    # Dealing Damage
    def attack(self, opponent):
        damage = self.attack_power
        print(f"{self.name} attacks {opponent.name} for {damage} damage!")
        opponent.take_damage(damage)
    
    # Taking Damage
    def take_damage(self, amount):
        # Block damage
        if self.block_next:
            print(f"{self.name} blocks the attack!")
            self.block_next = False
            return
        
        # Evades damage
        if self.evade_next:
            print(f"{self.name} evades the attack!")
            self.evade_next = False
            return
    
        # Guards damage
        if self.guard_next > 0:
            reduced = int(round(amount * (1 - self.guard_next)))
            print(f"{self.name} guards attack of {amount} to {reduced} damage!")
            amount = reduced
            self.block_next = 0.0
            return


        # Applying damage
        self.health -= amount
        if self.health < 0:
            self.health = 0

        print(f"{self.name} takes {amount} damage. ({self.health} / {self.max_health}) HP")

        if self.health <= 0:
            print(f"{self.name} has been vanquished!")
    
    # Healing Damage
    def heal(self):
        if self.heal_uses <= 0:
            print(f"{self.name} is out of healing uses!")
            return
        
        before = self.health
        self.health = min(self.max_health, self.health + self.heal_amount)
        self.heal_uses -= 1
        restored = self.health - before
        print(f"{self.name} heals for {restored} HP (uses left: {self.heal_uses})."
              f"\n{self.health}/{self.max_health}HP")
    
    # Stats
    def display_stats(self):
        print(
            f"\n{self.name}'s Stats:"
            f"\n======================="
            f"\nHealth: {self.health}/{self.max_health} HP"
            f"\nAttack: {self.attack_power}"
            f"\nHeal Uses: {self.heal_uses}"
            )
    
    # Using Class Abilities
    def get_abilities(self):
        return []
    def use_ability(self, idx, opponent):
        abilities = self.get_abilities()
        if idx < 1 or idx > len(abilities):
            print("Invalid ability choice.")
            return
        
        skill, skill_func = abilities[idx - 1]
        print(f"{self.name} uses {skill}!")
        skill_func(opponent)
    
# Player Classes
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=140, attack_power=30)

    # Skills
    def _power_strike(self, opponent):
        """150% more attack power hit"""
        damage = int(round(self.attack_power * 1.5))
        print(f"{self.name}'s Power Strike hits for {damage} damage!")
        opponent.take_damage(damage)

    def _rally(self, opponent):
        """Take 50% less damage from next hit"""
        self.guard_next = 0.5
        print(f"{self.name} rallies! Next incoming damage reduced by 50%.")

    def get_abilities(self):
        return [
            ("Power Strike (150% damage)", self._power_strike),
            ("Rally (50% damage reduction next hit)", self._rally),
        ]

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=35)

    # Skills
    def _fireball(self, opponent):
        """Range of attack multiplier 70% - 150%"""
        mult = random.uniform(0.7, 1.5)
        damage = int(round(self.attack_power * mult))
        print(f"{self.name} cast Fireball and erupts for {damage}!")
        opponent.take_damage(damage)

    def _ice_barrier(self, opponent):
        self.block_next = True
        print(f"{self.name} freezes the air around them creating an Ice Barrier! Next incoming damage is fully blocked.")

    def get_abilities(self):
        return [
            ("Fireball (70% - 150% damage)", self._fireball),
            ("Ice Barrier (Blocks next incoming damage)", self._ice_barrier),
        ]
    
class Hunter(Character):
    def __init__(self, name):
        super().__init__(name, health=125, attack_power=25)

    def _multi_shot(self, opponent):
        """Two Arrow shots of 70% damage"""
        shot = int(round(self.attack_power * .7))
        total = 0
        for i in range(2):
            print(f"{self.name}'s Multi-Shot arrow {i + 1} hits for {shot}!")
            opponent.take_damage(shot)
            total += shot
        print(f"Total Multi-Shot damage: {total}")

    def _evade(self,opponent):
        self.evade_next = True
        print(f"{self.name} prepares to Evade next attack!")

    def get_abilities(self):
        return [
            ("Multi-Shot (Two 70% damage arrows)", self._multi_shot),
            ("Evade (Next attack negated)", self._evade),
        ]


class Paladin(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=26)

    def _holy_strike(self,opponent):
        damage = self.attack_power + 10
        print(f"{self.name}'s Holy Strike smites for {damage}")
        opponent.take_damage(damage)

    def _divine_shield(self, opponent):
        self.block_next = True
        print(f"{self.name} emmits a Divine Shield around them! Next hit is negated!")

    def get_abilities(self):
        return [
            ("Holy Strike (Adds +10 damage)", self._holy_strike),
            ("Divine Shield (Negates next attack)", self._divine_shield)
        ]

# Enemy
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health=160, attack_power=15)

    def regenerate(self):
        regen = 5
        self.health = min(self.max_health, self.health + regen)
        print(f"{self.name} regenerates {regen} health! ({self.health}/{self.max_health} HP)")

    def attack(self, opponent):
        """Wizard attack with 20% chance of using special attack"""
        if random.random() < 0.2:
            damage = int(round(self.attack_power * 1.6))
            print(f"{self.name} hurls Shadow Blast for {damage} damage!")

        else:
            damage = self.attack_power
            print(f"{self.name} cast dark magic for {damage} damage!")
        opponent.take_damage(damage)

# Character Creation
def create_character():
    print("Choose your character class:")
    print("============================")
    print("1. Warrior")
    print("2. Mage")
    print("3. Hunter")
    print("4. Paladin")


    while True:
        class_choice = input("Enter the number of your class choice: ").strip()
        name = input("Enter your character's name: ").strip()

        if class_choice == "1":
            return Warrior(name)
        
        elif class_choice == "2":
            return Mage(name)
        
        elif class_choice == "3":
            return Hunter(name)
        
        elif class_choice == "4":
            return Paladin(name)
        
        else:
            print("Invalid choice. Please choose a number 1 - 4.")

# Player Actions
def choose_player_action(player):
    print("\n === Your Turn ===")
    print("1. Attack")
    print("2. Use Ability")
    print("3. Heal")
    print("4. View Stats")
    return input("Choose an action: ").strip()

# Calling functions
def choose_ability(player):
    abilities = player.get_abilities()
    if not abilities:
        print("No abilities available.")
        return None
    
    print("\nChoose an ability: ")
    for i, (skill, _) in enumerate(abilities, start=1):
        print(f"{i} {skill}")

    try:
        return int(input("Enter number: ").strip())
    except ValueError:
        print("Invalid input.")
        return None


# Battle Phase
def battle(player, opponent):
    print(f"\nA fearsome battle ensues! {player.name} Vs {opponent.name}\n")

    while opponent.health > 0 and player.health > 0:
        # Using "chose_player_action" function
        choice = choose_player_action(player)

        if choice == "1":
            player.attack(opponent)

        elif choice == "2":
            idx = choose_ability(player)
            if idx is not None:
                player.use_ability(idx, opponent)

        elif choice == "3":
            player.heal()

        elif choice == "4":
            player.display_stats()
            opponent.display_stats()

        else:
            print("Invalid input. Choose valid choice.")

        # If player wins
        if opponent.health <= 0:
            print(f"\nVictory! {opponent.name} has been slain by {player.name}!")
            break

        # Opponent Phase
        print("\n=== Opponent's Turn ===")
        if hasattr(opponent, "regenerate"):
            opponent.regenerate()
        opponent.attack(player)

        # If player loses
        if player.health <= 0:
            print(f"\nDefeat... {player.name} has been slain in battle!")
            break

# Playing the game
def main():
    random.seed()
    player = create_character()
    opponent = EvilWizard("Dark Sorcerer Sauron")
    battle(player, opponent)

if __name__ == "__main__":
    main()