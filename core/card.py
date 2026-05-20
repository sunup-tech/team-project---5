# core/card.py
import random

class Card:
    """낱장 카드를 정의하는 클래스"""

    def __init__(self, suit, rank):

        self.suit = suit
        self.rank = rank

    def __str__(self):

        return f"{self.suit}{self.rank}"


class Deck:
    """52장의 카드 덱"""

    def __init__(self):

        self.suits = ['♠', '◆', '♥', '♣']

        self.ranks = [
            'A', '2', '3', '4', '5',
            '6', '7', '8', '9', '10',
            'J', 'Q', 'K'
        ]

        self.cards = []

        self.reset()

    def reset(self):

        self.cards = [
            Card(suit, rank)
            for suit in self.suits
            for rank in self.ranks
        ]

        random.shuffle(self.cards)

    def draw(self):

        if len(self.cards) == 0:

            self.reset()

        return self.cards.pop()

    def __len__(self):

        return len(self.cards)