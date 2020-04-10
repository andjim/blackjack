from random import choice
from cards import Card, DECK
import re
from random import randint
from os import system
from wrapper import Wrapper

WP = Wrapper("",40,20)

class Hand(list):
   
    def add_card(self, card):
        if not isinstance(card, Card):
            raise ValueError('Must be Card type value')
        self.append(card)
    
    def empty_hand(self):
        self.clear()

    def __str__(self):
        res = ""
        for c in self:
            res += "%s, " % c
        return res

    @property
    def total(self):
        t = sum([c.value for c in self if not isinstance(c.value, tuple)])
        t += sum([ t > 10 and c.value[0] or c.value[1] for c in self if isinstance(c.value, tuple)])
        return t
    
class Player:

    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.hand = Hand()

    def hit(self, card):
        if not isinstance(card, (Card)): return False
        self.hand.append(card)
        return card

    def bet(self, amount):
        if not isinstance(amount, (int)):
            return False
        if amount < 1 or amount > self.money:
            return False

        self.money -= amount
        return amount

class Dealer(Player):
    def hit(self, card):
        if any([x for x in  self.hand if not x.faced]):
            c = self.hand.index(list(filter(lambda x: not x.faced, self.hand))[0])
            self.hand[c].faced = True
            return self.hand[c]
        return super(Dealer,self).hit(card)

    def choose(self,positive,negative):
        return self.hand.total > 5 and negative or positive
          
            
class Game:

    def __init__(self):
        self.deck = []
        self.state = {
            'on_bet': 0,
            'active_player': None,
            'finished': False,
            'over': False,
            'dealer': -1
        }
        self.players = [Dealer('Dealer',20000)]

    def shuffle(self):
        self.deck = sorted(self.deck, key=lambda c: randint(0, len(self.deck)))

    def _screen(self):
        data = {
            'active_player': self.state.get('active_player', False) and self.state['active_player'].name or '',
            'on_bet':  self.state.get('on_bet', False) and self.state['on_bet'] or 0
        }
        header = "Player's turn: %(active_player)s ||| BlackJack ||| On bet: %(on_bet)s\n\n" % (data)
        body = {
            'name': '',
            'cards': '',
            'money': '',
            'total': ''
        }
        for p in self.players:
            body['name'] +=  (not body['name']  and "{p.name} ||| " or " ||| {p.name}\n\n").format(p=p)
            body['cards'] += (not body['cards'] and "Cards: {p.hand} ||| " or " ||| Cards: {p.hand}\n").format(p=p)
            body['money'] += (not body['money'] and "Money: {p.money} ||| " or " ||| Money: {p.money}\n").format(p=p)
            body['total'] += (not body['total'] and "Total: {p.hand.total} ||| " or " ||| Total:{p.hand.total}\n").format(p=p)

        temp = header
        for l in body.values():
            temp += l
        WP.raw_text = temp
        system('clear')
        print(WP.wrap())

    def get_input(self, placeholder, validator):
        if not isinstance(placeholder, (str)): raise ValueError('Placeholder must be str')
        if not callable(validator): raise ValueError('validator must be a function')
        self._screen()
        value = validator(input('%s' % (placeholder)))
        return value

    def show_output(self, output):
        self._screen()
        print(output or '')
        input('Press any key to continue...')
        return 0

    def add_player(self):
        name = ""
        while not name:
            name = input("Your name: ")
        p = Player(name, 10000)
        self.players.insert(0,p)

    def first_draw(self):
        for p in self.players:
            for i in [1,0]:
                if not isinstance(p, Dealer):
                    p.hand.add_card(self.deck.pop())
                    continue
                c = self.deck.pop()
                c.faced = bool(i)
                p.hand.add_card(c)

    def bet(self):
        for p in self.players:
            if isinstance(p, (Dealer)): continue
            self.state['active_player'] = p
            while True:
                amount = self.get_input("bet: $", lambda x: (x and x.isnumeric() and int(x) or False ))
                if not p.bet(amount):
                    self.show_output('Amount should be a number below money')
                    continue
                self.state['on_bet'] = amount + self.players[self.state['dealer']].bet(amount)
                break
    
    def reset(self):
        self.state.update({
            'finisher': None,
            'on_bet': 0
        })
        for p in self.players:
            p.hand.empty_hand()

    def start(self):
        self.add_player()
        while not self.state['over']:
            self.deck = DECK * 2
            self.shuffle()
            self.bet()
            self.first_draw()
            winners = []
            for p in self.players:
                self.state['active_player'] = p
                while p.hand.total < 21 and not self.state.get('finisher', False):
                    ans = ''
                    while not ans:
                        ans = isinstance(p, Dealer) and p.choose('0','1') or \
                            self.get_input("wil hit [0] or stand [1]", lambda x: x in ('0', '1') and x or '') 
                        if not ans: self.show_output("input must be 1 for stand or 0 for hit")
                    if ans != '0': break
                    card = p.hit(self.deck.pop())
                    self.show_output("%s hitted and got %s" % (p.name, card))
                if not p.hand.total < 21:
                    self.state['finisher'] = p
            
            if not self.state.get('finisher', False):
                winners = list(filter(lambda p: p.hand.total > self.players[self.state['dealer']].hand.total,self.players )) or\
                    [self.players[self.state['dealer']],]
            else:
                winners = self.state['finisher'].hand.total == 21 and [self.state['finisher'],] or \
                    list(filter(lambda p: p != self.state['finisher']), self.players)

            cut = self.state['on_bet'] // len(winners)
            for w in winners:
                w.money += cut
                self.state['on_bet'] -= cut
                self.show_output('%s won and earned $%s' % (w.name, cut))

            self.state['active_player'] = False
            if not [p for p in self.players if p.money < 1]:
                
                self.state['over'] = self.get_input('Enter [1] to continue on table or just press enter to get out: ', 
                    lambda x: x != '1' and True or False
                )
                self.reset()
                continue
            for p in filter(lambda p: not isinstance(p, Dealer),self.players):
                self.show_output("Player %s exit table with $%s" % (p.name, p.money))
            self.state['over'] = True


if __name__ == "__main__":
    game = Game()
    game.start()


