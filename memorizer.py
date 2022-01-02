#######################################################################
#                           Memorizer Class                           #
#######################################################################

# Imports
from round import Round, WinType
import pickle
import time


class Memorizer:
    #################
    #  Constructor  #
    #################
    def __init__(self, opponents: list, current_round: int = 0, log: bool = True):
        # TODO: Hash oponents' names to avoid unparsable chars
        self.o_names = opponents
        self.rounds = []
        self.current_round = current_round
        self.log = log

    # =============
    # = New Round =
    # =============
    def new_round(self, round_number: int) -> None:
        self.current_round = int(round_number) - 1
        rs = {}
        for name in self.o_names:
            rs[name] = 0
        self.rounds.append(Round(round_number, ante=0, opponents=rs))

    # ==============================
    # = Update player's chip count =
    # ==============================
    def update_player_chips(self, player: str, chips: int) -> None:
        self.rounds[self.current_round].opponents[player].update_chips(chips)

    # =============================
    # = Update current round Ante =
    # =============================
    def update_ante(self, chips: int) -> None:
        self.rounds[self.current_round].ante = chips

    # ==============
    # = Forced bet =
    # ==============
    def forced_bet(self, player: str, chips: int) -> None:
        self.rounds[self.current_round].opponents[player].forced_bet(chips)

    # ===============
    # = Player open =
    # ===============
    def open(self, player: str, chips: int) -> None:
        self.rounds[self.current_round].opponents[player].open(chips)

    # ================
    # = Player Check =
    # ================
    def check(self, player: str, chips: int) -> None:
        self.rounds[self.current_round].opponents[player].check(chips)

    # ================
    # = Player Raise =
    # ================
    # chips: amount raised to
    def raise_to(self, player: str, chips: int) -> None:
        self.rounds[self.current_round].opponents[player].raise_to(chips)

    # ===============
    # = Player Call =
    # ===============
    def call(self, player: str) -> None:
        self.rounds[self.current_round].opponents[player].call()

    # ================
    # = Player Folds =
    # ================
    def fold(self, player: str) -> None:
        self.rounds[self.current_round].opponents[player].fold()

    # =================
    # = Player ALl-In =
    # =================
    def all_in(self, player: str, chips: int) -> None:
        self.rounds[self.current_round].opponents[player].all_in(chips)

    # ===============
    # = Player draw =
    # ===============
    def draw(self, player: str, card_count: int) -> None:
        self.rounds[self.current_round].opponents[player].draw(card_count)

    # =================================
    # = Round over - Winner announced =
    # =================================
    def round_over(self, wtype: WinType, player: str, amount: int) -> None:
        self.rounds[self.current_round].over(wtype, player, amount)

    # =============
    # = Game over =
    # =============
    def game_over(self) -> None:
        if self.log:
            fname = "dumps/dump_" + str(time.time()) + ".log"
            fdump = open(fname, "ab")
            pickle.dump(self.rounds, fdump)
            fdump.close()
            print("Log File dumped correctly")

    # ==================
    # = Hand reveladed =
    # ==================
    # during showdown
    def hand_revealed(self, player: str, hand: list) -> None:
        self.rounds[self.current_round].opponents[player].label_hand(hand)
