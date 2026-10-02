import numpy as np
import random


# 16 mult jokers 
add_mult_pool = {
    "Misprint": lambda h, d, t: random.randint(0,23),
    "Joker": lambda h, d, t: 4,
    "Jolly Joker": lambda h, d, t: 8 if t == "Pair" else 0,
    "Droll Joker": lambda h, d, t: 10 if t == "Flush" else 0,
    "Mad joker": lambda h, d, t: 10 if t == "Two Pair" else 0,
    "Crazy Joker": lambda h, d, t: 12 if t == "Straight" else 0,
    "Zany Joker": lambda h, d, t: 12 if t == "Three of a Kind" else 0,
    "Mystic Summit": lambda h ,d, t: 15 if d == 0 else 0,
    "Half Joker": lambda h,d ,t: 20 if len(h) <= 3 else 0,
    "Shoot The Moon": lambda h, d, t: sum([13 if card['rank']== "Queen" else 0 for card in h]),
    "Gluttonous Joker": lambda h, d, t: sum([3 if card["suit"] == "Clubs" else 0 for card in h]),
    "Greedy Joker": lambda h, d, t: sum([3 if card["suit"] == "Diamonds" else 0 for card in h]),
    "Even Steven": lambda h, d, t: sum([4 if card["order"] % 2 == 0 else 0 for card in h]),
    "Lusty Joker": lambda h, d, t: sum([3 if card["suit"] == "Hearts" else 0 for card in h]),
    "Wrathful Joker": lambda h, d, t: sum([3 if card["suit"] == "Spades" else 0 for card in h]),
    "Smiley Face": lambda h, d, t: sum([5 if card["rank"] in ["King", "Queen", "Jack"] else 0 for card in h])
    }
# 8 add_chips Jokers 
add_chips_pool = {
    "Banner": lambda h, d, t: 30*d,
    "Sly joker": lambda h, d, t: 50 if t == "Pair" else 0,
    "Crafty Joker": lambda h, d, t: 80 if t == "Flush" else 0,
    "Clever Joker": lambda h ,d ,t: 80 if t == "Two Pair" else 0,
    "Devious Joker" : lambda h, d, t: 100 if t == "Straight" else 0,
    "Willy Joker": lambda h, d, t: 100 if t == "Three of a Kind" else 0,
    "Odd Todd": lambda h, d, t: sum([15 if card["order"] % 2 != 0 else 0 for card in h]),
    "Scary Face": lambda h, d, t: sum([30 if card["rank"] in ["King", "Queen", "Jack"] else 0 for card in h])   
}

def apply_jokers(Jokers, hand, discards_remaining, hand_type):
    joker_mult = 0
    joker_chip_add = 0
    for joker in Jokers:
        if joker == "RTB":
            continue
        elif joker in add_mult_pool.keys():
            joker_mult += add_mult_pool[joker](hand, discards_remaining, hand_type)
        else:
            joker_chip_add += add_chips_pool[joker](hand, discards_remaining, hand_type)
    return joker_mult, joker_chip_add



def sample_joker(Jokers):
    if len(Jokers) >= 5:
        return Jokers
    

    owned = set(Jokers)

    available_mult = [joker for joker in add_mult_pool.keys() if joker is not owned]
    available_chips = [joker for joker in add_chips_pool.keys() if joker not in owned]

    sample_nums = random.randint(0,23) #24 jokers, 0 can be drawn, as can 23, so we dont include 24.
    
    if sample_nums > 7:
        joker = random.choice(list(add_mult_pool.keys()))[0]
        if not available_mult:
            return Jokers
        joker = random.choice(available_mult)
    else:
        if not available_chips:
            if not available_mult:
                return Jokers
            joker = random.choice(list(add_chips_pool.keys()))[0]
        else:
            joker = random.choice(available_chips)

    Jokers.append(joker)
    return Jokers



