#######################################################################
#                  FAST BIASED COMPUTED ACTION CLASS                  #
#######################################################################

# Imports
import enum
import math


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
            if seen != c:
                seen = c
            else:
                return c
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
            if c not in seen:
                seen.append(c)
            else:
                pairs.append(c)
                seen.remove(c)
        return pairs  # no pairs

    #######################################################################
    #                         Losing probability                          #
    #######################################################################
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

    @staticmethod
    def _having_2pair(hand: list) -> float:
        print("given: ", hand)
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
            + FB_cAction.HandRanks.THREE_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT.value[1]
            + FB_cAction.HandRanks.FLUSH.value[1]
            + FB_cAction.HandRanks.FULL_HOUSE.value[1]
            + FB_cAction.HandRanks.FOUR_OF_A_KIND.value[1]
            + FB_cAction.HandRanks.STRAIGHT_FLUSH.value[1]
            + FB_cAction.HandRanks.ROYAL_FLUSH.value[1]
        )


# print(FB_cAction._having_pair(["3c", "Tc", "3c", "Aj", "Th"]))
# print(FB_cAction._having_pair(["2c", "5s", "5s", "8j", "Th"]))
# print(FB_cAction._having_2pair(["2c", "5s", "5s", "8j", "Th"]))
# print(FB_cAction.get_pair(["3c", "Tc", "3c", "Aj", "Th"]))
# print(FB_cAction.get_pairs(["5c", "Tc", "3c", "Tc", "Th"]))
