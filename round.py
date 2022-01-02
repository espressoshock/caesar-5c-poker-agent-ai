#######################################################################
#                             Round Class                             #
#######################################################################

# Imports
from player import Player
import enum

##################
#  Victory type  #
##################
class WinType(enum.Enum):
    UNDISPUTED = (0,)
    DISPUTED = 1


class Round:
    #################
    #  Constructor  #
    #################
    # opponents: {name: chips}
    # number: server round number
    def __init__(self, number: int, ante: int, opponents: list):
        self.number = number
        self.ante = ante

        # =============
        # = Opponents =
        # =============
        # for simplicity
        # access actions
        # directly
        self.opponents = {name: Player(chips) for name, chips in opponents}

        # =================
        # = Round Results =
        # =================
        # available after
        # showdown
        self.results = None

    # =======================
    # = Update player chips =
    # =======================
    def update_chips(self, player: str, chips: int) -> None:
        self.opponents[player].update_chips(chips)

    # ===============
    # = Update ante =
    # ===============
    def update_ante(self, chips: int) -> None:
        self.ante = chips

    # ========================
    # = Winner been selected =
    # ========================
    def over(self, wtype: WinType, player: str, amount: int) -> None:
        self.results = {"w_type": wtype, "p_name": player, "w_amount": amount}
