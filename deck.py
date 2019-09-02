from random import choice
from cards import Card, DECK
import re
import subprocess as sp

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
    pass

class Game:
    deck = []
    on_bet = 0
    players =[Dealer('Dealer',1000000)]
        
    def shuffle(self):
        cards = []
        for c in self.deck:
            card_index = self.deck.index(choice(self.deck))
            card = self.deck.pop(card_index)
            cards.append(card)
        self.deck = cards
    
    def bet(self):
        for player in self.players:
            self.on_bet += player.bet()
    
    def turn(self):
        res = {}
        for player in self.players:
            player_info = {'player':player, 'status': 'play'}
            last_card = None
            while True:
                hitted = player.hit()
                player_info.update(hitted=hitted)
                if not hitted:
                    player_info.update(card= last_card)
                    break

                last_card = self.deck.pop()
                player.hand.add_card(last_card)
                player_info.update(card= last_card)

                print(player.hand.total)
                if player.hand.total > 21:
                    player_info.update(status='lost')
                    break
                elif player.hand.total == 21:
                    player_info.update(status="won")
                    break
            res = player_info
        return res

    def _will_play(self):
        while True:
            play:str = input('Would you play? ([1]: yes [0]: no): ')
            if not play.isdigit():
                print("%s was not a valid asnwer, use 1 for yes or 0 for no." % play)
                continue
            return bool(int(play))
        

    def start(self):
        while True:
            if not self._will_play():
                break
            self.deck = DECK * 2 # two decks of fifty-two cards
            self.bet()
            self.shuffle()
            while True:
                last_player_info = self.turn()
                
                if last_player_info.get('status') != 'play':
                    print('%s has %s' % (last_player_info.get('player').name,last_player_info.get('status')))
                    break
                
                winner = sorted(self.players, key=lambda x: x.hand.total, reverse=True)[0]
                if winner:
                   print('%s has %s' % (last_player_info.get('player').name,last_player_info.get('won')))
                   break
                

if __name__ == "__main__":
    game = Game()
    game.start()





