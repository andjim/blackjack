from random import choice
from cards import Card, DECK
import re
from random import choice
from os import system
from wrapper import Wrapper

WP = Wrapper("",40,40)

class Hand(list):
   
    def add_card(self, card):
        if not isinstance(card, Card):
            raise ValueError('Must be Card type value')
        self.append(card)
    
    def _sort_card(self):
        cards = []
        for c in self:
            if not isinstance(c.value, tuple):
                cards.insert(-1,c)
                continue
            cards.append(c)
        self = Hand(cards)
    
    def empty_hand(self):
        self.clear()

    def __str__(self):
        res = ""
        for c in self:
            res += "%s, " % c
        return res

    @property
    def total(self):
        total = 0
        self._sort_card()
        for c in self:
            if not isinstance(c.value, tuple):
                total += c.value
                continue
            # [1,11]
            total += c.value[0] if total > 10 else c.value[1]
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
                print('Bet above your funds.\n')
                continue
            
            self.money -= amount
            return amount

    
class Dealer(Player):
    def hit(self):
        if self.hand.total >= 17:
            return False
        return True

class Game:
    deck = []
    state = {
        'on_bet': 0,
        'active_player': None
    }
    players = [Dealer('Dealer',20000)]

    def shuffle(self):
        cards = []
        for c in self.deck:
            card_index = self.deck.index(choice(self.deck))
            card = self.deck.pop(card_index)
            cards.append(card)
        self.deck = cards

    def screen(self, func):
        system('clear')
        data = {
            'active_player': self.players[self.state['active_player']].name,
            'on_bet': self.state['on_bet']
        }
        header = "Player's turn: %(active_player)s ||| BlackJack ||| On bet: %(on_bet)s\n\n" % (data)
        body = {
            'name': '',
            'cards': '',
            'money': '',
            'total': ''
        }
        players = self.players[0:]
        players.reverse()
        for p in players:
            body['name'] +=  (not body['name']  and "{p.name} ||| " or " ||| {p.name}\n\n").format(p=p)
            body['cards'] += (not body['cards'] and "Cards: {p.hand} ||| " or " ||| Cards: {p.hand}\n").format(p=p)
            body['money'] += (not body['money'] and "Money: {p.money} ||| " or " ||| Money: {p.money}\n").format(p=p)
            body['total'] += (not body['total'] and "Total: {p.hand.total} ||| " or " ||| Total:{p.hand.total}\n").format(p=p)

        temp = header
        for l in body.values():
            temp += l
        WP.raw_text = temp
        print(WP.wrap())
        func(2)

    def add_player(self):
        name = ""
        while not name:
            name = input("Your name: ")
        p = Player(name, 10000)
        self.players.append(p)

    def first_draw(self):
        for p in self.players:
            for i in [1,0]:
                if not isinstance(p, Dealer):
                    p.hand.add_card(self.deck.pop())
                    continue
            c = self.deck.pop()
            c.faced = bool(i)
            p.hand.add_card(c)  

    def start(self):
        self.deck = DECK * 2
        self.shuffle()
        self.add_player()
        self.first_draw()


if __name__ == "__main__":
    game = Game()
    game.start()





