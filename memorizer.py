#######################################################################
#                           Memorizer Class                           #
#######################################################################

# Imports
from round import Round


class Memorizer:
    #################
    #  Constructor  #
    #################
    def __init__(self, opponents: list, current_round: int = 0):
        self.o_names = opponents
        self.rounds = []
        self.current_round = current_round

    # =============
    # = New Round =
    # =============
    def new_round(self, round_number: int) -> None:
        self.current_round = round_number
        rs = {}
        for o in self.o_names:
            rs = {o: 0}
        self.rounds.append(Round(round_number, ante=0, opponents=rs))

    # ==============================
    # = Update player's chip count =
    # ==============================
    def update_player_chips(self, player: str, chips: int) -> None:
        self.rounds[self.current_round].oponents[player].update_chips(chips)

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
    def round_over(self, wtype: Round.Win_Type, player: str, amount: int) -> None:
        self.rounds[self.current_round].over(wtype, player, amount)
