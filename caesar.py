#######################################################################
#                       👑 Caesar Agent 👑                            #
#######################################################################

# =Imports
import numpy as np

# faster than our implementation
from phevaluator import evaluate_cards


class Caesar:
    ############
    #  CONSTS  #
    ############
    DRAW_MONTECARLO_SAMPLES_N = 20000

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
    def _mc_ev_draw(
        self, hand: list, max_depth: int = 32, M: int = DRAW_MONTECARLO_SAMPLES_N
    ) -> int:
        # ======================
        # = Discards scenarios =
        # ======================
        # for speed precomputed
        # all scenarios
        # Discard   0, 1, 2,  3, 4, 5
        # C(n,r)    1, 5, 10,10, 5, 1
        # TODO: convert into N with bitmasking / O(N)->O(1)
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
        # =======================
        # = Monte Carlos G-Vars =
        # =======================
        mc_samples = np.empty((len(discards), M), dtype=object)
        mc_betas = np.zeros((len(discards), M))
        mc_beta_hats = np.zeros((len(discards)))
        # ===============
        # = Simulations =
        # ===============
        for idis in range(max_depth):
            # ====================
            # = Compute new hand =
            # ====================
            # compute hand with discards
            # TODO: might wanna use numpy for performances
            c_hand = []
            c_ndiscards = 0
            for i in range(len(hand)):
                if not discards[idis][i]:
                    c_hand.append(hand[i])  # better than copy+pop
                else:
                    c_ndiscards += 1  # cache this for later

            # ===================================
            # = Monte Carlo LRR with R-Sampling =
            # ===================================
            # add hybrid selection to reduce
            # search space
            for si in range(M):
                # ========================
                # = Compute replacements =
                # ========================
                c_hand_sample = [
                    x if x not in ["10h", "10d", "10s", "10c"] else "T" + x[2]
                    for x in c_hand
                ]
                # ============================
                # = No discards Special Case =
                # ============================
                # TODO: update this with analytical statistics
                #  no need ot waste cycles here
                if c_ndiscards == 0:
                    # compute directly current hand
                    mc_samples[idis][si] = (c_hand_sample, idis)
                    mc_betas[idis][si] = evaluate_cards(*c_hand_sample)
                    continue
                c_deck = self._build_new_deck(exclude=c_hand)
                rng = np.random.default_rng()
                sampled = rng.choice(c_deck, c_ndiscards, replace=False)
                c_hand_sample.extend(sampled)
                # ================================
                # = Monte Carlo Samples and Beta =
                # ================================
                mc_samples[idis][si] = (c_hand_sample, idis)
                mc_betas[idis][si] = evaluate_cards(*c_hand_sample)
            # ==============
            # = Compute β̂ =
            # ==============
            mc_beta_hats[idis] = np.mean(mc_betas)
        # =========================
        # = Compute best strategy =
        # =========================
        # TODO: Replace built-in sort with radix-sort
        # TODO: Add bluffing as hybrid meta-metric
        s_idis = np.argsort(mc_beta_hats)
        print("mc: ", mc_beta_hats)
        print("given hand: ", hand)
        print("best strategy found: ", s_idis[0], discards[s_idis[0]])

    #######################################################################
    #                                Utils                                #
    #######################################################################
    def _build_new_deck(self, exclude: list) -> list:
        suits = ["h", "d", "s", "c"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
        deck = [r + s for r in ranks for s in suits]
        # for c in exclude:
        #     deck.remove(c if c not in ["10h", "10d", "10s", "10c"] else "T" + c[2])
        # ==================
        # = Faster exclude =
        # ==================
        return self._fast_deck_update(deck, exclude)

    def _fast_deck_update(self, deck, exclude) -> list:
        return list(set(deck) - set(exclude))


c = Caesar()
c._mc_ev_draw(hand=["Ac", "As", "Ad", "Ah", "5c"], M=1000)
# hand = ["Qs", "8s", "Js", "Qc", "Ks"]
# ndeck = c._build_new_deck(exclude=hand)
# print("deck:, ", ndeck, len(ndeck))
