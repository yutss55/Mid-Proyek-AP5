# Model for character
class Character:
    def __init__(self, user_id: int, class_name: str, hp: int, energy: int, defense: int, damage: int):
        self.user_id = user_id
        self.class_name = class_name
        self.hp = hp
        self.energy = energy
        self.defense = defense
        self.damage = damage
        self.gold = 10
        self.exp = 0
        self.floor = 1
        self.title = "Novice"
        self.score = 0
        self.inventory = {}

def show_status(self):
        print(f"=== STATUS KARAKTER ===")
        print(f"Class   : {self.class_name}")
        print(f"HP      : {self.hp}")
        print(f"Energy  : {self.energy}")
        print(f"Defense : {self.defense}")
        print(f"Damage  : {self.damage}")
        print(f"Gold    : {self.gold}")
        print(f"EXP     : {self.exp}")
        print(f"Floor   : {self.floor}")
        print(f"Title   : {self.title}")
        print(f"Score   : {self.score}")
        print(f"Inventory: {self.inventory}")

