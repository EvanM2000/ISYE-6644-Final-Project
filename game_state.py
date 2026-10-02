import random
from dataclasses import dataclass, field
from states import deck
from states import joker
import sys
import os
import hand_selection

@dataclass # https://docs.python.org/3/library/dataclasses.html#dataclasses.field
class GameState():
    base_chips = {1: 300,
                   2: 800,
                   3: 2000,
                   4: 5000,
                   5: 11000,
                   6: 20000,
                   7: 35000,
                   8: 50000}
    
    
    use_rtb: bool = False
    use_rtb_in_sim: bool = False
    deck_type: str = "Red_Deck"
    ante: int = 1
    hand_size: int = 8
    hands_remaining: int = 4
    debuffed_suits: set = field(default_factory=set) #this is used to specify the base of this field, because it is mutabel depending on debuff
    hand_levels: str = "Small_Blind"
    add_mult: int = 0
    rtb_streak: int = 0
    played_hand_types: list = field(default_factory=list)
    blinds_played: int = 0
    discarded_cards: list = field(default_factory = list)
    discards_remaining: int = 3
    play_deck: object = field(default_factory=deck.Deck)
    hand_number : int = 0
    game_over: bool = False
    won : bool = False
    num_jokers: int = 0
    Jokers: list = field(default_factory = list)
    use_Jokers: bool = False
    chip_mult_dict = { #[base chip score, mult]
        "Straight Flush": [100, 8],
        "Four of a Kind" : [60, 7],
        "Full House" : [40, 4],
        "Flush" : [35, 4],
        "Straight": [30, 4],
        "Three of a Kind": [30, 3],
        "Two Pair": [20, 2],
        "Pair": [10, 2],
        "High Card": [5, 1]
    }

    
    def target_score(self):
        base = self.base_chips[self.ante]
        if self.hand_levels == "Small_Blind":
            return base
        elif self.hand_levels == "Big_Blind":
            return base * 1.5
        elif self.hand_levels == "Boss_Blind":
            return base * 2

    def play_blind(self):
        chips_won = 0
        hands_allowed = 5 if self.deck_type == "Blue" else 4
        self.discards_remaining = 4 if self.deck_type == "Red" else 3

        to_beat = self.target_score()
        for _ in range(hands_allowed):
            if chips_won >= to_beat:
                break
            hand = self.play_deck.deal_hand()
            
            hand, self.discards_remaining, _, self.discarded_cards, _ = hand_selection.discard_decision(hand, self.discards_remaining, self.use_rtb, self.discarded_cards, self.play_deck)
            #print(f"Before select_hand: self.use_rtb={self.use_rtb}, self.add_mult={self.add_mult}") #Claude suggestsed this print statement, please see the explanation below.
            best_hand, hand_type, chip_count, self.add_mult = hand_selection.select_hand(
                hand, self.add_mult if self.use_rtb else 0, self.use_rtb
            )
            #print(f"After select_hand: self.add_mult={self.add_mult}") # When debugging code, I explained the problem I was having to claude and this print statement was directly suggested by claude, but it did not prove to be helpful to the original programming poroblem. 
            #originally, I had an added game_state.py file I had not deleted, which I was using in my simulation.py file, Failure to check that I didn't have any old files had gotten me very confused. In laimens terms, the functions in here werent actually the ones being called in my simulation file for a while when I was initially crafting the code.

            joker_mult, joker_chip_add = joker.apply_jokers(self.Jokers, best_hand, self.discards_remaining, hand_type)

            chips_won += (sum(card["chips"] for card in best_hand)
                          + joker_chip_add
                          + self.chip_mult_dict[hand_type][0]) * (self.chip_mult_dict[hand_type][1]
                                                                  + self.add_mult
                                                                  + joker_mult)
            
            total_mult = self.add_mult +joker_mult + self.chip_mult_dict[hand_type][1]
            joker_chip_add
                                                                    
            self.hand_number += 1
            self.played_hand_types.append({
                "hand_number": self.hand_number,
                "discarded_cards": self.discarded_cards,
                "discards_used": len(self.discarded_cards),
                "hand": best_hand,
                "hand_type": hand_type,
                "add_mult_from_RTB" : self.add_mult,
                "tot_Jokers_mults": total_mult,
                "add_chips_from_Jokers": joker_chip_add,
                "chips_won": chips_won,
                "ante": self.ante,
                "blind": self.hand_levels})
            self.discarded_cards = []
        self.blinds_played += 1 
        return chips_won >= to_beat, chips_won # chips_won >= is a booleon, dictating whether or not we won round
    
    def advance_blind(self, won):
        if won == False:
            self.game_over = True
            return self.played_hand_types


        if self.hand_levels == "Small_Blind" and self.blinds_played == 1:
            if self.use_rtb_in_sim == True:
                  self.use_rtb = True #toggled on after round 1 it on after round 1 
                  self.Jokers.append("RTB") 
                  self.hand_levels = "Big_Blind"
            else:
                self.hand_levels = "Big_Blind"
                if len(self.Jokers) < 5 and self.use_Jokers == True:
                    self.Jokers = joker.sample_joker(self.Jokers)

        elif self.hand_levels == "Small_Blind":
            if len(self.Jokers) < 5 and self.use_Jokers == True :
                self.Jokers = joker.sample_joker(self.Jokers)
            self.hand_levels = "Big_Blind"

        elif self.hand_levels == "Big_Blind":
            if len(self.Jokers) < 5 and self.use_Jokers == True:
                self.Jokers = joker.sample_joker(self.Jokers)
            self.hand_levels = "Boss_Blind"

        else:
            self.hand_levels = "Small_Blind"
            if len(self.Jokers) < 5 and self.use_Jokers == True:
                self.Jokers = joker.sample_joker(self.Jokers)
            self.ante += 1 
            if self.ante >8:
                self.game_over = True
                self.won = True
                return 
        self.play_deck = deck.Deck()
        self.discards_remaining = 3
        self.discarded_cards = []




                




            


     
    


    




