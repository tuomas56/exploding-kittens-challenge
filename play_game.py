#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is heavily based on an example of the library pyCardDeck.
It is taken from: https://pycarddeck.readthedocs.io/en/latest/examples/kittens.html

There is no point in changing this file as this is what will be used for the
evaluation of your solution.
"""

import pyCardDeck
from pyCardDeck.cards import BaseCard
from random import randrange, shuffle
import importlib
from sys import argv
from base_player import BasePlayer


class KittenCard(BaseCard):
    def __init__(self, name: str, targetable: bool = False, selfcast: bool = False):
        super().__init__(name)
        self.selfcast = selfcast
        self.targetable = targetable
    def effect(self, player: BasePlayer, target: BasePlayer, game: Game):
        pass

class ExplodeCard(KittenCard):
    def __init__(self, name: str = "Exploding Kitten"):
        super().__init__(name)

class DefuseCard(KittenCard):
    def __init__(self, deck: pyCardDeck.deck, name: str = "Defuse"):
        super().__init__(name, selfcast=True)
        self.deck = deck
    def effect(self, player: BasePlayer, target: BasePlayer, game: Game):
        position = player.insert_explode()
        self.deck.add_single(ExplodeCard(), position=position)

class TacocatCard(KittenCard):
    def __init__(self, name: str = "Tacocat"):
        super().__init__(name)

class OverweightCard(KittenCard):
    def __init__(self, name: str = "Overweight Bikini Cat"):
        super().__init__(name)

class CatsSchrodinger(KittenCard):
    def __init__(self, name: str = "Cat's Schrodinger"):
        super().__init__(name)

class ShuffleCard(KittenCard):
    def __init__(self, deck: pyCardDeck.Deck, name: str = "Shuffle"):
        super().__init__(name)
        self.deck = deck
    def effect(self, player: BasePlayer, target: BasePlayer, game: Game):
        self.deck.shuffle()

class AttackCard(KittenCard):
    def __init__(self, name: str = "Attack"):
        super().__init__(name, selfcast=True, targetable=True)
    def effect(self, player: BasePlayer, target: BasePlayer, game: Game):
        player.skip()
        target.take_turn_twice(game)

class SeeTheFuture(KittenCard):
    def __init__(self, deck: pyCardDeck.Deck, name: str = "See The Future"):
        super().__init__(name)
        self.deck = deck
    def effect(self, player: BasePlayer, target: BasePlayer, game: Game):
        return self.deck.show_top(3)

class NopeCard(KittenCard):
    def __init__(self, name: str = "Nope"):
        super().__init__(name)

class SkipCard(KittenCard):
    def __init__(self, name: str = "Skip"):
        super().__init__(name, selfcast=True)
    def effect(self, player: BasePlayer, target: BasePlayer, game: Game):
        player.skip()

class FavorCard(KittenCard):
    def __init__(self, name: str = "Favor"):
        super().__init__(name, targetable=True, selfcast=True)
    def effect(self, player: BasePlayer, target: BasePlayer, game: Game):
        random_target_card = target.hand.pop(randrange(target.hand))
        player.hand.append(random_target_card)

class Game:

    def __init__(self, players: list, verbose: bool=True):
        self.verbose = verbose
        self.deck = pyCardDeck.Deck()
        self.players = players
        self.prepare_cards()
        self.deck.shuffle()
        self.deal_to_players()
        self.add_defuses()
        self.add_explodes()
        self.deck.shuffle()
        self.last_card = None
        #print([c.name for c in self.deck])
        while 1 < len(self.players) < len(self.deck):
            self.play()
        if self.verbose: print('The winner is', self.players[0].name)

    def play(self):
        i = 0
        while i < len(self.players):
            self.players[i].use_hand()
            self.players[i].hand.append(self.deck.draw())
            self.last_card = self.players[i].turn(self)
            if len(self.players[i].hand) > 0 and self.players[i].hand[-1].name == 'Exploding Kitten':
                if self.verbose: print('Player',self.players[i].name, 'explodes!!')
                del self.players[i]
            else:
                i += 1
        if self.verbose: print('Deck:',len(self.deck), [len(player.hand) for player in self.players])

    def turn(self):
        print('Turn not used!')

    def prepare_cards(self):
        if self.verbose: print("Preparing deck from which to deal to players")
        self.deck.add_many(construct_deck(self))

    def deal_to_players(self):
        if self.verbose: print("Dealing cards to players")
        for _ in range(4):
            for player in self.players:
                player.hand.append(self.deck.draw())

    def ask_for_nope(self):
        noped = False
        for player in self.players:
            noped = player.nope_prompt()
        return noped

    def add_explodes(self):
        if self.verbose: print("Adding explodes to the deck")
        self.deck.add_many([ExplodeCard() for _ in range(len(self.players) - 1)])

    def add_defuses(self):
        if self.verbose: print("Adding defuses to the deck")
        self.deck.add_many([DefuseCard(self.deck) for _ in range(6 - len(self.players))])

    def play_card(self, card: KittenCard, player: BasePlayer = None, target: BasePlayer = None):
        if card.selfcast and player is None:
            raise Exception("You must pass a player who owns the card!")
        elif card.targetable and target is None:
            raise Exception("You must pass a target!")
        elif not self.ask_for_nope():
            card.effect(player, target, self)
        else:
            pass


def construct_deck(game: Game):
    card_list = [
        TacocatCard(),
        TacocatCard(),
        TacocatCard(),
        TacocatCard(),
        OverweightCard(),
        OverweightCard(),
        OverweightCard(),
        OverweightCard(),
        CatsSchrodinger(),
        CatsSchrodinger(),
        CatsSchrodinger(),
        CatsSchrodinger(),
        ShuffleCard(game.deck),
        ShuffleCard(game.deck),
        ShuffleCard(game.deck),
        ShuffleCard(game.deck),
        AttackCard(),
        AttackCard(),
        AttackCard(),
        AttackCard(),
        SeeTheFuture(game.deck),
        SeeTheFuture(game.deck),
        SeeTheFuture(game.deck),
        SeeTheFuture(game.deck),
        SeeTheFuture(game.deck),
        NopeCard(),
        NopeCard(),
        NopeCard(),
        NopeCard(),
        NopeCard(),
        SkipCard(),
        SkipCard(),
        SkipCard(),
        SkipCard(),
        FavorCard(),
        FavorCard(),
        FavorCard(),
        FavorCard(),
    ]
    return card_list


all_modules = [[], []]
for i in range(1, len(argv)):
    module = importlib.import_module(argv[i])
    all_modules[0].append(module)
    all_modules[1].append(argv[i])

print('Starting with',len(all_modules[0]),'players...')

hall_of_fame = {}
for trials in range(1000):
    all_players = []
    for module, player_name in zip(all_modules[0],all_modules[1]):
        all_players.append(module.Player(player_name))
    shuffle(all_players)
    game = Game(all_players,verbose=False)
    winner = game.players[0].name

    if winner not in hall_of_fame.keys():
        hall_of_fame[winner] = 0
    hall_of_fame[winner] += 1

print('Result:', hall_of_fame)

"""
zaf = Player()
jara = Player()
alex = Player()
game = Game([zaf,jara,alex])
"""











#
