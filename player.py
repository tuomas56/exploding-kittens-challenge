#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an example of pyCardDeck, it's not meant to be complete poker script,
but rather a showcase of pyCardDeck's usage.
"""

import pyCardDeck
from pyCardDeck.cards import BaseCard
from random import randrange
import numpy as np 


class Player:
    def __init__(self):
        self.hand = []

    def turn(self):
        if self.hand[-1].name == 'Exploding Kitten':
            print('A player might explode..')
            for card in self.hand:
                if card.name == 'Defuse':
                    self.hand.pop()
                    card.effect(self,self)
    def skip(self):
        pass

    def take_turn_twice(self):
        self.turn()
        self.turn()

    def nope_prompt(self) -> bool:
        for card in self.hand:
            if card.name == "Nope":
                if input("Do you want to use your Nope card?").lower().startswith("y"):
                    return True
                else:
                    return False
        return False

    def insert_explode(self) -> int:
        #position = int(input("At which position from top do you want to insert Exploding Kitten back into the deck?"))
        position = np.random.randint(2)
        return position


class KittenCard(BaseCard):

    def __init__(self, name: str, targetable: bool = False, selfcast: bool = False):
        super().__init__(name)
        self.selfcast = selfcast
        self.targetable = targetable

    def effect(self, player: Player, target: Player):
        pass


class ExplodeCard(KittenCard):

    def __init__(self, name: str = "Exploding Kitten"):
        super().__init__(name)


class DefuseCard(KittenCard):

    def __init__(self, deck: pyCardDeck.deck, name: str = "Defuse"):
        super().__init__(name, selfcast=True)
        self.deck = deck

    def effect(self, player: Player, target: Player):
        position = player.insert_explode()
        self.deck.add_single(ExplodeCard(), position=position)


class TacocatCard(KittenCard):

    def __init__(self, name: str = "Tacocat"):
        super().__init__(name)


class OverweightCard(KittenCard):

    def __init__(self, name: str = "Overweight Bikini Cat"):
        super().__init__(name)


class ShuffleCard(KittenCard):

    def __init__(self, deck: pyCardDeck.Deck, name: str = "Shuffle"):
        super().__init__(name)
        self.deck = deck

    def effect(self, player: Player, target: Player):
        self.deck.shuffle()


class AttackCard(KittenCard):

    def __init__(self, name: str = "Attack"):
        super().__init__(name, selfcast=True, targetable=True)

    def effect(self, player: Player, target: Player):
        player.skip()
        target.take_turn_twice()


class SeeTheFuture(KittenCard):

    def __init__(self, deck: pyCardDeck.Deck, name: str = "See The Future"):
        super().__init__(name)
        self.deck = deck

    def effect(self, player: Player, target: Player):
        self.deck.show_top(3)


class NopeCard(KittenCard):

    def __init__(self, name: str = "Nope"):
        super().__init__(name)


class SkipCard(KittenCard):

    def __init__(self, name: str = "Skip"):
        super().__init__(name, selfcast=True)

    def effect(self, player: Player, target: Player):
        player.skip()


class FavorCard(KittenCard):

    def __init__(self, name: str = "Favor"):
        super().__init__(name, targetable=True, selfcast=True)

    def effect(self, player: Player, target: Player):
        random_target_card = target.hand.pop(randrange(target.hand))
        player.hand.append(random_target_card)


class Game:

    def __init__(self, players: list):
        self.deck = pyCardDeck.Deck()
        self.players = players
        self.prepare_cards()
        self.deal_to_players()
        self.add_defuses()
        self.add_explodes()
        while 1 < len(self.players) < len(self.deck):
            self.play()
        print('The winner is', self.players[0])

    def play(self):
        i = 0
        while i < len(self.players):
            self.players[i].hand.append(self.deck.draw())
            self.players[i].turn()
            if len(self.players[i].hand) > 0 and self.players[i].hand[-1].name == 'Exploding Kitten':
                print('Player',self.players[i], 'explodes!!')
                del self.players[i]
            else:
                i += 1
        print('Deck:',len(self.deck), [len(player.hand) for player in self.players])

    def turn(self):
        print('Turn not used!')

    def prepare_cards(self):
        print("Preparing deck from which to deal to players")
        self.deck.add_many(construct_deck(self))

    def deal_to_players(self):
        print("Dealing cards to players")
        for _ in range(4):
            for player in self.players:
                player.hand.append(self.deck.draw())

    def ask_for_nope(self):
        noped = False
        for player in self.players:
            noped = player.nope_prompt()
        return noped

    def add_explodes(self):
        print("Adding explodes to the deck")
        self.deck.add_many([ExplodeCard() for _ in range(len(self.players) - 1)])

    def add_defuses(self):
        print("Adding defuses to the deck")
        self.deck.add_many([DefuseCard(self.deck) for _ in range(6 - len(self.players))])

    def play_card(self, card: KittenCard, player: Player = None, target: Player = None):
        if card.selfcast and player is None:
            raise Exception("You must pass a player who owns the card!")
        elif card.targetable and target is None:
            raise Exception("You must pass a target!")
        elif not self.ask_for_nope():
            card.effect(player, target)
        else:
            print("Card was noped :(")


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


print('Starting..')


#import jaras_file

zaf = Player()
jara = Player()
alex = Player()

game = Game([zaf,jara,alex])











#
