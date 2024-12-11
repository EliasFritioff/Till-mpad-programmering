#ELIAS TEINF22 / klar

import os

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        
    def __str__(self):
        return f"{self.value} {self.suit}"
    
    
class Deck:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards
        
    def show_all(self):
        for card in self.cards:
            if card.suit == "♥" or card.suit == "♦": 
                print(f"\033[31m{card}\033[0m")
            else:
                print(f"{card}")

    @staticmethod
    def make_deck():  
        cards = [] 
        suits = ["♠", "♥", "♣", "♦"]
        values = ["Ess", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        
        for suit in suits:
            for value in values:
                cards.append(Card(suit, value))
        
        return cards


os.system('cls' if os.name == 'nt' else 'clear')

cards = Deck.make_deck()

deck = Deck(cards)

deck.show_all()