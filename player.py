#######################################################################
#                   Player Class | Memorizer Module                   #
#######################################################################

# Imports
from action import Action, Type


class Player:
    #################
    #  Constructor  #
    #################
    def __init__(self, chips: int = 0):
        self.chips = chips
        self.actions = []

        # =================
        # = Revealed hand =
        # =================
        # labelled data
        # only available after
        # showdown
        # used for regression
        # correlation coeff.
        self.hand = []

    # ================
    # = Update chips =
    # ================
    def update_chips(self, chips: int) -> None:
        self._chips = chips

    # ==============
    # = Forced bet =
    # ==============
    def forced_bet(self, chips: int) -> None:
        self.actions.append(Action(Type.FORCED_BET, chips))

    # ===============
    # = Player open =
    # ===============
    def open(self, chips: int) -> None:
        self.actions.append(Action(Type.PLAYER_OPEN, chips))

    # ================
    # = Player Check =
    # ================
    def check(self, chips: int) -> None:
        self.actions.append(Action(Type.PLAYER_CHECK, chips))

    # ================
    # = Player Raise =
    # ================
    # chips: amount raised to
    def raise_to(self, chips: int) -> None:
        self.actions.append(Action(Type.PLAYER_RAISE, chips))

    # ===============
    # = Player Call =
    # ===============
    def call(self) -> None:
        self.actions.append(Action(Type.PLAYER_RAISE))

    # ================
    # = Player Folds =
    # ================
    def fold(self) -> None:
        self.actions.append(Action(Type.PLAYER_FOLD))

    # =================
    # = Player ALl-In =
    # =================
    def all_in(self, chips: int) -> None:
        self.actions.append(Action(Type.PLAYER_ALL_IN, chips))

    # ===============
    # = Player draw =
    # ===============
    def draw(self, card_count: int) -> None:
        self.actions.append(Action(Type.PLAYER_DRAW, card_count))

    # =========================
    # = Label opponent's hand =
    # =========================
    # available after showdown
    def label_hand(self, hand: list) -> None:
        self.hand = hand
