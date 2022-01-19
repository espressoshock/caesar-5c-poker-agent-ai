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
    def __init__(self, number: int, ante: int, opponents: dict):
        self.number = number
        self.ante = ante

        # =============
        # = Opponents =
        # =============
        # for simplicity
        # access actions
        # directly
        self.opponents = {name: Player(chips) for name, chips in opponents.items()}

        # =================
        # = Round Results =
        # =================
        # available after
        # showdown
        self.results = None

        # ============
        # = Pot size =
        # ============
        # Better cache
        # than retrieve
        self.pot = 0
        self.c_call = 0

    # ===================
    # = Update Pot size =
    # ===================
    def update_pot(self, pot: int) -> None:
        self.pot += pot

    # ===========================
    # = Update Pot size by Call =
    # ===========================
    def update_pot_call(self) -> None:
        self.pot += self.c_call

    # =======================
    # = Update Current call =
    # =======================
    def update_call(self, call: int) -> None:
        self.c_call = call

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
