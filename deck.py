import random

class Deck(object):
    def __init__(self):
        self.create_deck()
        self.shuffle_deck()
        self.played_this_ante = []
    
    def create_deck(self):
        ranks= ['2', '3', '4', '5', '6',
            '7', '8', '9', '10', 'Jack',
            'Queen', 'King', 'Ace']
        
        straight_values = [2, 3, 4, 5, 6,
                           7, 8, 9, 10, 11,
                           12, 13, 14]

        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.deck = [{'rank': rank, 'suit': suit, 'order': order, 'chips': int(rank) if rank.isdigit()
              else 10 if rank in ['Jack', 'Queen', 'King'] else 11}
             for suit in suits for rank, order in zip(ranks, straight_values)]

    
    def shuffle_deck(self):
        random.shuffle(self.deck)
        # random uses a  Mersenne Twister Algorithm, with 53-bit precision float and has a period of
        # 2**19937-1, which is a very long period, meaning it will take a very long time before we have repeating numbers!
        #which is a psuedo random number generation, but it seeds from my Operating system.
        #documentation: https://docs.python.org/3/library/random.html
        return self
    
    def deal_hand(self):
        hand = self.deck[0:8]
        self.deck = self.deck[8:]
        return hand
    
    def draw_cards(self, num):
        draw = self.deck[0:num]
        self.deck = self.deck[num:]
        return draw
    



    

    
    def record_played(self, ranks):
        self.played_this_ante.extend(ranks)

