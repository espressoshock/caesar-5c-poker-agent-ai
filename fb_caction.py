#######################################################################
#                  FAST BIASED COMPUTED ACTION CLASS                  #
#######################################################################

# Imports
import enum
import math

# faster than my implementation
from phevaluator import evaluate_cards as evc


class FB_cAction:
    #######################
    #  HAND RANK CLASSES  #
    #######################
    # max ranges
    class HandRanks(enum.Enum):
        # (class range, probability)
        # precomputed hypergeometric dist.
        ROYAL_FLUSH = (1, 0.0000015391)
        STRAIGHT_FLUSH = (10, 0.0000138517)
        FOUR_OF_A_KIND = (166, 0.0002400960)
        FULL_HOUSE = (322, 0.0014405762)
        FLUSH = (1599, 0.0019654015)
        STRAIGHT = (1609, 0.0039246468)
        THREE_OF_A_KIND = (2467, 0.0211284514)
        TWO_PAIR = (3325, 0.0475390156)
        PAIR = (6185, -1)  # don't play this
        HIGH_CARD = (7462, -1)

    ###################
    #  Gateway proxy  #
    ###################
    @staticmethod
    def describe(hand: list) -> dict:
        gateway = {
            FB_cAction.HandRanks.PAIR: FB_cAction._having_pair,
            FB_cAction.HandRanks.TWO_PAIR: FB_cAction._having_2pair,
            FB_cAction.HandRanks.THREE_OF_A_KIND: FB_cAction._having_3ok,
            FB_cAction.HandRanks.STRAIGHT: FB_cAction._having_straight,
            FB_cAction.HandRanks.FLUSH: FB_cAction._having_flush,
            FB_cAction.HandRanks.FULL_HOUSE: FB_cAction._having_full_house,
            FB_cAction.HandRanks.FOUR_OF_A_KIND: FB_cAction._having_4ok,
            FB_cAction.HandRanks.STRAIGHT_FLUSH: FB_cAction._having_straight_flush,
            FB_cAction.HandRanks.ROYAL_FLUSH: FB_cAction._having_royal_flush,
        }
        # =======================
        # = Return context loss =
        # =======================
        return {
            "loss": gateway.get(FB_cAction.hand_value(evc(*hand)), -1)(hand),
            "win": 1 - gateway.get(FB_cAction.hand_value(evc(*hand)), -1)(hand),
        }

    #######################################################################
    #                                Utils                                #
    #######################################################################

    # =============================
    # = Hand value from Hand rank =
    # =============================
    @staticmethod
    def hand_value(hand_rank: int) -> "HandRanks":
        if hand_rank == FB_cAction.HandRanks.ROYAL_FLUSH.value[0]:
            return FB_cAction.HandRanks.ROYAL_FLUSH
        elif hand_rank <= FB_cAction.HandRanks.STRAIGHT_FLUSH.value[0]:
            return FB_cAction.HandRanks.STRAIGHT_FLUSH
        elif hand_rank <= FB_cAction.HandRanks.FOUR_OF_A_KIND.value[0]:
            return FB_cAction.HandRanks.FOUR_OF_A_KIND
        elif hand_rank <= FB_cAction.HandRanks.FULL_HOUSE.value[0]:
            return FB_cAction.HandRanks.FULL_HOUSE
        elif hand_rank <= FB_cAction.HandRanks.FLUSH.value[0]:
            return FB_cAction.HandRanks.FLUSH
        elif hand_rank <= FB_cAction.HandRanks.STRAIGHT.value[0]:
            return FB_cAction.HandRanks.STRAIGHT
        elif hand_rank <= FB_cAction.HandRanks.THREE_OF_A_KIND.value[0]:
            return FB_cAction.HandRanks.THREE_OF_A_KIND
        elif hand_rank <= FB_cAction.HandRanks.TWO_PAIR.value[0]:
            return FB_cAction.HandRanks.TWO_PAIR
        elif hand_rank <= FB_cAction.HandRanks.PAIR.value[0]:
            return FB_cAction.HandRanks.PAIR

        return FB_cAction.HandRanks.HIGH_CARD

    # ==============================
    # = Get highest card from hand =
    # ==============================
    @staticmethod
    def get_max(hand: list) -> str:
        values = dict(zip("23456789TJQKA", range(2, 15)))

        def sortkey(x):
            value, suit = x
            return values[value], suit

        return sorted(hand, key=sortkey, reverse=True)[0]

    @staticmethod
    def get_pair(hand: list) -> str:
        values = dict(zip("23456789TJQKA", range(2, 15)))

        def sortkey(x):
            value, suit = x
            return values[value], suit

        srt = sorted(hand, key=sortkey, reverse=True)
        seen = ""
        for c in srt:
            if seen != c[0]:
                seen = c[0]
            else:
                return c[0]
        return None  # no pairs

    @staticmethod
    def get_pairs(hand: list) -> str:
        values = dict(zip("23456789TJQKA", range(2, 15)))

        def sortkey(x):
            value, suit = x
            return values[value], suit

        srt = sorted(hand, key=sortkey, reverse=True)
        seen = []
        pairs = []
        for c in srt:
            if c[0] not in seen:
                seen.append(c[0])
            else:
                pairs.append(c[0])
                seen.remove(c[0])
        return pairs  # no pairs

    @staticmethod
    def get_3ok(hand: list) -> str:
        values = dict(zip("23456789TJQKA", range(2, 15)))

        def sortkey(x):
            value, suit = x
            return values[value], suit

        srt = sorted(hand, key=sortkey, reverse=True)
        seen = {}
        for c in srt:
            seen[c[0]] = seen.get(c[0], 0) + 1
            if seen[c[0]] == 3:
                return c[0]

        return None  # no pairs

    @staticmethod
    def get_4ok(hand: list) -> str:
        values = dict(zip("23456789TJQKA", range(2, 15)))

        def sortkey(x):
            value, suit = x
            return values[value], suit

        srt = sorted(hand, key=sortkey, reverse=True)
        prev = ""
        for c in srt:
            if c[0] == prev:
                return c[0]
            else:
                prev = c[0]

        return None  # no pairs

    @staticmethod
    def get_sorted_hand(hand: list) -> list:
        values = dict(zip("23456789TJQKA", range(2, 15)))

        def sortkey(x):
            value, suit = x
            return values[value], suit

        return sorted(hand, key=sortkey, reverse=True)

    #######################################################################
    #                         Losing probability                          #
    #######################################################################
    # =========================
    # = High hand v High Hand =
    # =========================
    # E[x]
    @staticmethod
    def _high_v_high(hand: list) -> float:
        # ==========
        # = Params =
        # ==========
        s_hand = FB_cAction.get_sorted_hand(hand)
        all_comb = math.comb(52, 5)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        return (
            (_diffs(s_hand[0]) * 4)
            + (_diffs(s_hand[1]) * 4)
            + (_diffs(s_hand[2]) * 4)
            + (_diffs(s_hand[3]) * 4)
            + (_diffs(s_hand[4]) * 4)
        ) / all_comb

    # =================
    # = Having a Pair =
    # =================
    @staticmethod
    def _having_pair(hand: list) -> float:
        # ==========
        # = Params =
        # ==========
        max_card = FB_cAction.get_max(hand)
        pair = FB_cAction.get_pair(hand)
        all_comb = math.comb(52, 5)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        ncr42 = math.comb(4, 2)
        ncr123 = math.comb(12, 3)
        better_pair = (_diffs(pair) * ncr42 * ncr123 * (4 ** 3)) / all_comb
        higher = (_diffs(max_card) * 4) / all_comb

        return (
            higher
            + better_pair
            + FB_cAction.HandRanks.TWO_PAIR.value[1]
            + FB_cAction.HandRanks.THREE_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT.value[1]
            + FB_cAction.HandRanks.FLUSH.value[1]
            + FB_cAction.HandRanks.FULL_HOUSE.value[1]
            + FB_cAction.HandRanks.FOUR_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )

    # ==================
    # = Having 2 Pairs =
    # ==================
    @staticmethod
    def _having_2pair(hand: list) -> float:
        print("given: ", hand)
        # ==========
        # = Params =
        # ==========
        max_card = FB_cAction.get_max(hand)
        pairs = FB_cAction.get_pairs(hand)
        all_comb = math.comb(52, 5)
        print("pairs: ", pairs)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        ncr42 = math.comb(4, 2)
        ncr123 = math.comb(12, 3)
        better_pair = (_diffs(pairs) * ncr42 * ncr123 * (4 ** 3)) / all_comb
        higher = (_diffs(max_card) * 4) / all_comb

        return (
            higher
            + better_pair
            + FB_cAction.HandRanks.THREE_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT.value[1]
            + FB_cAction.HandRanks.FLUSH.value[1]
            + FB_cAction.HandRanks.FULL_HOUSE.value[1]
            + FB_cAction.HandRanks.FOUR_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )

    # ======================
    # = Having 3 of a Kind =
    # ======================
    @staticmethod
    def _having_3ok(hand: list) -> float:
        print("given: ", hand)
        # ==========
        # = Params =
        # ==========
        tok = FB_cAction.get_3ok(hand)
        all_comb = math.comb(52, 5)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        ncr43 = math.comb(4, 3)
        ncr122 = math.comb(12, 2)
        better_3ok = (_diffs(tok + "x") * ncr43 * ncr122 * (4 ** 2)) / all_comb

        return (
            +better_3ok
            + FB_cAction.HandRanks.STRAIGHT.value[1]
            + FB_cAction.HandRanks.FLUSH.value[1]
            + FB_cAction.HandRanks.FULL_HOUSE.value[1]
            + FB_cAction.HandRanks.FOUR_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )

    # ===================
    # = Having Straight =
    # ===================
    @staticmethod
    def _having_straight(hand: list) -> float:
        print("given: ", hand)
        # ==========
        # = Params =
        # ==========
        max_card = FB_cAction.get_max(hand)
        all_comb = math.comb(52, 5)
        print("max: ", max_card)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        better_straight = ((_diffs(max_card) * (4 ** 5)) - (10 * 4)) / all_comb

        return (
            +better_straight
            + FB_cAction.HandRanks.FLUSH.value[1]
            + FB_cAction.HandRanks.FULL_HOUSE.value[1]
            + FB_cAction.HandRanks.FOUR_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )

    # ==================
    # = Having a Flush =
    # ==================
    @staticmethod
    def _having_flush(hand: list) -> float:
        print("given: ", hand)
        # ==========
        # = Params =
        # ==========
        s_hand = FB_cAction.get_sorted_hand(hand)
        all_comb = math.comb(52, 5)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        better_flush = ((_diffs(s_hand[0]) * 4 ** 5) - (10 * 4)) / all_comb
        higher = FB_cAction._high_v_high(s_hand)

        return (
            better_flush
            + higher
            + FB_cAction.HandRanks.FULL_HOUSE.value[1]
            + +FB_cAction.HandRanks.FOUR_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )

    # =====================
    # = Having full house =
    # =====================
    @staticmethod
    def _having_full_house(hand: list) -> float:
        print("given: ", hand)
        # ==========
        # = Params =
        # ==========
        tok = FB_cAction.get_3ok(hand)
        suits = ["c", "d", "h", "s"]
        rm = [tok + s for s in suits]
        pair = FB_cAction.get_pair(set(hand).difference(set(rm)))
        all_comb = math.comb(52, 5)
        print("tok and pair", tok, pair)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        ncr43 = math.comb(4, 3)
        ncr42 = math.comb(4, 2)
        better_3ok = (_diffs(tok + "x") * ncr43 * 12 * ncr42) / all_comb
        better_pair = (_diffs(pair + "x") * 12 * ncr43 * ncr42) / all_comb

        return (
            +better_3ok
            + better_pair
            + +FB_cAction.HandRanks.FOUR_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )

    # ======================
    # = Having 4 of a Kind =
    # ======================
    @staticmethod
    def _having_4ok(hand: list) -> float:
        print("given: ", hand)
        # ==========
        # = Params =
        # ==========
        fok = FB_cAction.get_4ok(hand)
        all_comb = math.comb(52, 5)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        better_4ok = (_diffs(fok + "x") * 12 * 4) / all_comb

        return (
            +better_4ok
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )

    # ===========================
    # = having a Straight Flush =
    # ===========================
    @staticmethod
    def _having_straight_flush(hand: list) -> float:
        print("given: ", hand)
        # ==========
        # = Params =
        # ==========
        max_card = FB_cAction.get_max(hand)
        all_comb = math.comb(52, 5)

        # =========
        # = Cases =
        # =========
        def _diffs(x):
            diffs = dict(zip("AKQJT98765432", range(0, 13)))
            value, suit = x
            return diffs[value]

        better_straight_flush = (_diffs(max_card) * 4) / all_comb

        return better_straight_flush + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]

    # ========================
    # = Having a Royal Flush =
    # ========================
    @staticmethod
    def _having_royal_flush(hand: list) -> float:
        return 0.0


# print(FB_cAction._having_pair(["3c", "Tc", "3c", "Aj", "Th"]))
# print(FB_cAction._having_pair(["2c", "5s", "5s", "8j", "Th"]))
# print(FB_cAction._having_2pair(["2c", "5s", "5s", "2j", "Th"]))
# print(FB_cAction._having_3ok(["2c", "Ts", "3s", "Tc", "Th"]))
# print(FB_cAction._having_4ok(["5c", "5s", "5d", "5h", "Th"]))
# print(FB_cAction._having_straight(["3c", "4s", "5s", "6c", "7h"]))
# print(FB_cAction._having_full_house(["Tc", "4s", "Ts", "4c", "Th"]))
# print(FB_cAction._having_straight_flush(["5c", "6c", "7c", "8c", "9h"]))
# print(FB_cAction._high_v_high(["5c", "6c", "7c", "8c", "9h"]))
# print(FB_cAction._having_flush(["2c", "Qc", "7c", "8c", "9c"]))
# print(FB_cAction.get_pair(["3c", "Tc", "3c", "As", "Th"]))
# print(FB_cAction.get_pairs(["3c", "Tc", "3c", "Tc", "Th"]))
# print(FB_cAction.get_3ok(["2d", "Ts", "3s", "Tc", "Th"]))
# print(FB_cAction.get_4ok(["5c", "5s", "5d", "5h", "Th"]))

# print(FB_cAction._having_flush(["2c", "Qc", "7c", "8c", "9c"]))
# print(FB_cAction.describe(["2c", "Qc", "7c", "8c", "9c"]))
