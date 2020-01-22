class Card:
    _value = None
    def __init__(self, name, suit, value):
        self.name = name
        self.suit = suit
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        if isinstance(val, int) and val > 0:
            self._value = val
        elif isinstance(val, tuple) and len(val) == 2:
            self._value = val
        else:
            raise ValueError('Worng value %s' % (val))

    def __str__(self):
        return "%s of %s" % (self.name,self.suit)


CARDS_TEMPLATE = [
    {
        'name':'A',
        'suit':'',
        'value': (1,11),
    },
    {
        'name':'Two',
        'suit':'',
        'value': 2,
    },
    {
        'name':'Three',
        'suit':'',
        'value': 3,
    },
    {
        'name':'Four',
        'suit':'',
        'value': 4,
    },
    {
        'name':'Five',
        'suit':'',
        'value': 5,
    },
    {
        'name':'Six',
        'suit':'',
        'value': 6,
    },
    {
        'name':'Seven',
        'suit':'',
        'value': 7,
    },
    {
        'name':'Eight',
        'suit':'',
        'value': 8,
    },
    {
        'name':'Nine',
        'suit':'',
        'value': 9,
    },
    {
        'name':'Ten',
        'suit':'',
        'value': 10,
    },
    {
        'name':'J',
        'suit':'',
        'value': 10,
    },
    {
        'name':'Queen',
        'suit':'',
        'value': 10,
    },
    {
        'name':'King',
        'suit':'',
        'value': 10,
    },
]

def deck_generator():
    suits = ['Hearts','Diamonds','Spades', 'Clubs']
    deck = []
    for suit in suits:
        for card in CARDS_TEMPLATE:
            deck.append(Card(card['name'], suit, card['value']))

    return deck

DECK = deck_generator()
