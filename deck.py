from random import choice
import re

class Card:
    _value = None
    def __init__(self, name, band, value):
        self.name = name
        self.band = band
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, int) and val < 0:
            self._value = val
        elif isinstance(val, tuple) and len(val) == 2:
            self._value = val
        else:
            raise ValueError('Worng value')

class Hand:
    _cards = []

    @property
    def cards(self):
        self._cards
    
    def add_card(self, card):
        if not isinstance(card, Card):
            raise ValueError('Must be Card type value')
        self._cards.append(card)
    
    def _sort_card(self):
        cards = []
        for c in self._cards:
            if not isinstance(c.value, tuple):
                cards.insert(-1,c)
                continue
            cards.append(c)
        self._cards = cards

    @property
    def total(self):
        total = 0
        self._sort_card()
        for c in self._cards:
            if not isinstance(c.value, tuple):
                total += c.value
                continue
            # [1,11]
            total = c.value[0] if total > 10 else c.value[1]
        return total 
            
    
class Player:

    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = Hand()

    def hit(self):
        options = {'stand':'^[sS][tT][aA][nN][dD]$','hit':'^[hH][iI][tT]$'}
        while True:
            answer:str = input('Would you hit or stand: ')

            if re.search(options['stand'], answer):
                return False

            elif re.search(options['hit'], answer):
                return True

            else:
                print("Your answer must be 'hit' or 'stand'")
                continue
            

    def bet(self):
        while True:
            amount:str = input("Your bet: $")
            if not amount.isnumeric():
                print('Bet must be numbers.\n')
                continue
            amount = int(amount)
            if amount < 1:
                print('Bet must be higher than 1.\n')
                continue

            if amount > self.money:
                print('Bet above your funds 1.\n')
                continue
            
            self.money -= amount
            return amount

    
class Dealer(Player):
    pass

class Game:
    deck = [] #just for now
    on_bet = 0
    player = None
    dealer = None

    def shuffle(self):
        cards = []
        for c in self.deck:
            cards.append(self.deck.pop(choice(self.deck)))
        self.deck = cards
    
    def bet(self):
        self.on_bet += self.player.bet() * 2
    
    def hit(self):
        players = [self.dealer, self.player]
        for player in players:
            if not player.hit():
                print("%s standed." % player.name)
                print("%s's turn has passed.\n" % player.name)
                continue
            card = self.deck.pop()
            player.hand.add_card(card)
            print("%s hitted and obtained %s" % (card.name))
            print("%s's turn has passed.\n" % player.name)


