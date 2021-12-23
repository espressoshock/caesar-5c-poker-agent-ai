#######################################################################
#                       👑 Caesar Agent 👑                            #
#######################################################################

# =Imports
import numpy as np

# faster than our implementation
from phevaluator import evaluate_cards


class Caesar:
    class Exchange:
        def __init__(self, hand: list):
            self.cards = hand
            self.count = 0

    ###########
    #  Props  #
    ###########
    @property
    def name(self):
        return "Caesar"

    ###################
    #  Draw Strategy  #
    ###################
    # Hybrid optimized
    # monte-carlo variation
    def _mc_ev_draw(self, hand: list, M: int = 20000) -> int:
        # ======================
        # = Discards scenarios =
        # ======================
        # for speed precomputed
        # all scenarios
        # Discard   0, 1, 2,  3, 4, 5
        # C(n,r)    1, 5, 10,10, 5, 1
        discards = np.array(
            [
                # discard 0
                [0, 0, 0, 0, 0],
                # discard 1 (5)
                [1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 0],
                [0, 0, 0, 0, 1],
                # discard 2 (10)
                [1, 1, 0, 0, 0],
                [1, 0, 1, 0, 0],
                [1, 0, 0, 1, 0],
                [1, 0, 0, 0, 1],
                [0, 1, 1, 0, 0],
                [0, 1, 0, 1, 0],
                [0, 1, 0, 0, 1],
                [0, 0, 1, 1, 0],
                [0, 0, 1, 0, 1],
                [0, 0, 0, 1, 1],
                # discard 3 (10)
                [1, 1, 1, 0, 0],
                [1, 1, 0, 1, 0],
                [1, 1, 0, 0, 1],
                [1, 0, 0, 1, 1],
                [1, 0, 1, 0, 1],
                [1, 0, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 0, 1, 1],
                [0, 1, 1, 0, 1],
                [0, 0, 1, 1, 1],
                # discard 4 (5)
                [1, 1, 1, 1, 0],
                [1, 1, 1, 0, 1],
                [1, 1, 0, 1, 1],
                [1, 0, 1, 1, 1],
                [0, 1, 1, 1, 1],
                # discard 5 (1)
                [1, 1, 1, 1, 1],
            ]
        )
        # ===============
        # = Simulations =
        # ===============

    #######################################################################
    #                                Utils                                #
    #######################################################################
    def _get_new_deck(self, exclude: list) -> list:
        suits = ["h", "d", "s", "c"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        deck = [r + s for r in ranks for s in suits]
        for c in exclude:
            deck.remove(c)
        return deck


c = Caesar()
# c._mc_ev_draw(hand=["Qs", "5h", "Ac", "8s", "4d"])
# ndeck = c._get_new_deck(["Qs", "5h", "Ac", "8s", "4d"])
# print("deck:, ", ndeck, len(ndeck))
