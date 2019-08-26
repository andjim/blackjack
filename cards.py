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
        if isinstance(val, int) and val > 0:
            self._value = val
        elif isinstance(val, tuple) and len(val) == 2:
            self._value = val
        else:
            raise ValueError('Worng value %s' % (val))


CARDS_TEMPLATE = [
    {
        'name':'A',
        'band':'',
        'value': (1,11),
    },
    {
        'name':'Two',
        'band':'',
        'value': 2,
    },
    {
        'name':'Three',
        'band':'',
        'value': 3,
    },
    {
        'name':'Four',
        'band':'',
        'value': 4,
    },
    {
        'name':'Five',
        'band':'',
        'value': 5,
    },
    {
        'name':'Six',
        'band':'',
        'value': 6,
    },
    {
        'name':'Seven',
        'band':'',
        'value': 7,
    },
    {
        'name':'Eight',
        'band':'',
        'value': 8,
    },
    {
        'name':'Nine',
        'band':'',
        'value': 9,
    },
    {
        'name':'Ten',
        'band':'',
        'value': 10,
    },
    {
        'name':'J',
        'band':'',
        'value': 10,
    },
    {
        'name':'Queen',
        'band':'',
        'value': 10,
    },
    {
        'name':'King',
        'band':'',
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
