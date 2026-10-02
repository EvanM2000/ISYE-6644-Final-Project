from collections import Counter
import csv
import hand_selection as hand_selection
import states.game_state
from states.game_state import GameState
import pandas as pd

def simulation(use_rtb_in_sim = False, deck_type = "Red", replications = 50, use_Jokers = False):
    results = []
    all_hands = []

    for run_id in range(replications):
        game = GameState(use_rtb_in_sim = use_rtb_in_sim, deck_type = deck_type, use_Jokers = use_Jokers)
        while not game.game_over:
            won, _ = game.play_blind()
            game.advance_blind(won)
        
        for hand_record in game.played_hand_types:
            hand_record["run_id"] = run_id
            all_hands.append(hand_record)

        hands_by_ante = {}
        for h in game.played_hand_types:
            hands_by_ante.setdefault(h['ante'], []).append(h['hand_type'])
        most_played = {
            f"most_played_hand_ante_{a}": Counter(types).most_common(1)[0][0]
            for a, types in hands_by_ante.items()
        }

        avg_chips_by_ante = {}
        for a, types in hands_by_ante.items():
            ante_hands = [h for h in game.played_hand_types if h['ante'] == a]
            avg_chips_by_ante[f"avg_chips_ante_{a}"] = sum(h['chips_won'] for h in ante_hands) / len(ante_hands)

        result_row = {
            "run_id": run_id,
            "jokers": game.Jokers,
            "ante_reached": game.ante,
            "blinds_played": game.blinds_played,
            "won": game.won,
            "use_rtb": game.use_rtb_in_sim,
            "deck_type": game.deck_type,
            "avg_chips_per_hand": sum(h["chips_won"] for h in game.played_hand_types) / len(game.played_hand_types) if game.played_hand_types else 0,
            "avg_Joker_chips" : sum(h["add_chips_from_Jokers"] for h in game.played_hand_types) / len(game.played_hand_types) if game.played_hand_types else 0,
            "avg_joker_mult": sum(h["tot_Jokers_mults"] for h in game.played_hand_types) / len(game.played_hand_types) if game.played_hand_types else 0,
            "avg_RTB_mult_per_hand": sum(h["add_mult_from_RTB"] for h in game.played_hand_types) / len(game.played_hand_types) if game.played_hand_types else 0,
            "total_discards": sum(h["discards_used"] for h in game.played_hand_types),
        }

        result_row.update(most_played)
        result_row.update(avg_chips_by_ante)
        results.append(result_row)


    return results, all_hands

def export_to_csv(results, all_hands, results_file="default_results.csv", hands_file = "default_hands.csv"):
    results_df = pd.DataFrame(results)
    results_df.to_csv(results_file, index=False)
    
    hands_df = pd.DataFrame(all_hands)
    hands_df.to_csv(hands_file, index=False)
    
    return results_df, hands_df

if __name__ == "__main__": #AI Generated, I had a hard time figuring out how to do this. Claude. 
    results, all_hands = simulation(use_rtb_in_sim = True, deck_type="Red", use_Jokers = True, replications=50000)
    results_df, hands_df = export_to_csv(results, all_hands, results_file = "RTB_Joker_results.csv", hands_file = "RTB_Joker_hands")

    print(f"Completed {len(results)} runs")
    print(f"Win rate: {results_df['won'].mean():.2%}")
    print(f"Max Ante: {results_df['ante_reached'].max():.2f}")
    print(f"Average chips per hand: {results_df['avg_chips_per_hand'].mean():.2f}")
    print(f"Max Jokers: {results_df['jokers'].apply(len).max()}")
    print(f"Average joker chip adds per hand : {results_df['avg_Joker_chips'].mean():.2f}")
    print(f"Average discards per hand: {hands_df['discards_used'].mean():.2f}")
    print(f"Average joker mult per hand: {results_df['avg_joker_mult'].mean():.2f}")
    print(f"Average RTB mult per hand: {results_df['avg_RTB_mult_per_hand'].mean():.2f}")
    print(f"Max Joker Mult: {hands_df['tot_Jokers_mults'].max()}")


    results, all_hands = simulation(use_rtb_in_sim = False, deck_type="Red", use_Jokers = False, replications=50000)
    results_df, hands_df = export_to_csv(results, all_hands, results_file = "default_results.csv", hands_file = "default_hands.csv")

    print(f"Completed {len(results)} runs")
    print(f"Win rate: {results_df['won'].mean():.2%}")
    print(f"Max Ante: {results_df['ante_reached'].max():.2f}")
    print(f"Average chips per hand: {results_df['avg_chips_per_hand'].mean():.2f}")
    print(f"Max Jokers: {results_df['jokers'].apply(len).max()}")
    print(f"Average joker chip adds per hand : {results_df['avg_Joker_chips'].mean():.2f}")
    print(f"Average discards per hand: {hands_df['discards_used'].mean():.2f}")
    print(f"Average joker mult per hand: {results_df['avg_joker_mult'].mean():.2f}")
    print(f"Average RTB mult per hand: {results_df['avg_RTB_mult_per_hand'].mean():.2f}")
    print(f"Max Joker Mult: {hands_df['tot_Jokers_mults'].max()}")

    results, all_hands = simulation(use_rtb_in_sim = False, deck_type="Red", use_Jokers = True, replications=50000)
    results_df, hands_df = export_to_csv(results, all_hands, results_file = "Jokers_results.csv", hands_file = "Jokers_hands.csv")
    
    print(f"Completed {len(results)} runs")
    print(f"Win rate: {results_df['won'].mean():.2%}")
    print(f"Max Ante: {results_df['ante_reached'].max():.2f}")
    print(f"Average chips per hand: {results_df['avg_chips_per_hand'].mean():.2f}")
    print(f"Max Jokers: {results_df['jokers'].apply(len).max()}")
    print(f"Average joker chip adds per hand : {results_df['avg_Joker_chips'].mean():.2f}")
    print(f"Average discards per hand: {hands_df['discards_used'].mean():.2f}")
    print(f"Average joker mult per hand: {results_df['avg_joker_mult'].mean():.2f}")
    print(f"Average RTB mult per hand: {results_df['avg_RTB_mult_per_hand'].mean():.2f}")
    print(f"Max Joker Mult: {hands_df['tot_Jokers_mults'].max()}")
    
    results, all_hands = simulation(use_rtb_in_sim = True, deck_type="Red", use_Jokers = False, replications=50000)
    results_df, hands_df = export_to_csv(results, all_hands, results_file = "RTB_only_results.csv", hands_file = "RTB_only_hands.csv")

    print(f"Completed {len(results)} runs")
    print(f"Win rate: {results_df['won'].mean():.2%}")
    print(f"Max Ante: {results_df['ante_reached'].max():.2f}")
    print(f"Average chips per hand: {results_df['avg_chips_per_hand'].mean():.2f}")
    print(f"Max Jokers: {results_df['jokers'].apply(len).max()}")
    print(f"Average joker chip adds per hand : {results_df['avg_Joker_chips'].mean():.2f}")
    print(f"Average discards per hand: {hands_df['discards_used'].mean():.2f}")
    print(f"Average joker mult per hand: {results_df['avg_joker_mult'].mean():.2f}")
    print(f"Average RTB mult per hand: {results_df['avg_RTB_mult_per_hand'].mean():.2f}")
    print(f"Max Joker Mult: {hands_df['tot_Jokers_mults'].max()}")
        
