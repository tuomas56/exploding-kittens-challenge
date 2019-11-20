class BasePlayer:
    def __init__(self, name):
        self.name = name
        self.hand = []
    def use_hand(self):
        pass
    def turn(self, game):
        pass
    def skip(self):
        pass
    def take_turn_twice(self, game):
        pass
    def nope_prompt(self):
        pass
    def insert_explode(self):
        pass
