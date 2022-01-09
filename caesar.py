#######################################################################
#                       👑 Caesar Agent 👑                            #
#######################################################################

# =Imports
from memorizer import Memorizer
from mc_cdraw import MC_CDraw
from fb_caction import FB_cAction
from game_config import AgentAction
import enum
import numpy as np


class Caesar:
    #################
    #  SEE(s) ENUM  #
    #################
    class See(enum.Enum):
        NEW_ROUND = (0,)
        GAME_OVER = (1,)
        PLAYER_CHIPS = (2,)
        ANTE_CHANGED = (3,)
        FORCED_BET = (4,)
        PLAYER_OPEN = (5,)
        PLAYER_CHECK = (6,)
        PLAYER_RAISE = (7,)
        PLAYER_CALL = (8,)
        PLAYER_FOLD = (9,)
        PLAYER_ALL_IN = (10,)
        PLAYER_DRAW = (11,)
        PLAYER_HAND = (12,)
        ROUND_OVER_UNDISPUTED = (13,)
        ROUND_OVER_DISPUTED = (14,)

    #################
    #  ACT(s) ENUM  #
    #################
    class Act(enum.Enum):
        OPEN = (0,)
        CALL_OR_RAISE = (1,)
        DRAW = (2,)

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

    #################
    #  Constructor  #
    #################
    def __init__(self, n_players: int = 5):
        # ==================
        # = Game Specifics =
        # ==================
        self.gs_nplayers = n_players

        # =============
        # = Memorizer =
        # =============
        self.memorizer = Memorizer([], 0, log=True)
        # ======================
        # = Registered Players =
        # ======================
        self.registered_players = dict()
        # ================
        # = Current hand =
        # ================
        hand = []

    #######################################################################
    #                               SEE(s)                                #
    #######################################################################
    def see(self, what: See, *args) -> None:
        print("what", what, args)
        gateway = {
            self.See.NEW_ROUND: self.memorizer.new_round,
            self.See.GAME_OVER: self.memorizer.game_over,
            self.See.PLAYER_CHIPS: self._player_chips_update,
            self.See.ANTE_CHANGED: self.memorizer.update_ante,
            self.See.FORCED_BET: self.memorizer.forced_bet,
            self.See.PLAYER_OPEN: self.memorizer.open,
            self.See.PLAYER_CHECK: self.memorizer.check,
            self.See.PLAYER_RAISE: self.memorizer.raise_to,
            self.See.PLAYER_CALL: self.memorizer.call,
            self.See.PLAYER_FOLD: self.memorizer.fold,
            self.See.PLAYER_ALL_IN: self.memorizer.all_in,
            self.See.PLAYER_DRAW: self.memorizer.draw,
            self.See.PLAYER_HAND: self.memorizer.hand_revealed,
            self.See.ROUND_OVER_UNDISPUTED: self.memorizer.round_over,
            self.See.ROUND_OVER_DISPUTED: self.memorizer.round_over,
        }
        if what == self.See.NEW_ROUND and args[0] < 2:
            return
        if what == self.See.PLAYER_HAND and args[0] == self.name:
            self.hand = args[1]
        return gateway.get(what, "Error: what not found")(*args)

    # ===========================
    # = To patch initial config =
    # ===========================
    def _player_chips_update(self, player, chips) -> None:
        if len(self.memorizer.rounds) < 1:
            self.registered_players[player] = chips
            if len(self.registered_players.keys()) == self.gs_nplayers:
                self.memorizer.o_names = list(self.registered_players.keys())
                self.memorizer.new_round(1)
                for _player, _chips in self.registered_players.items():
                    self.memorizer.update_player_chips(_player, int(_chips))
        else:
            self.memorizer.update_player_chips(player, int(chips))

    #######################################################################
    #                               ACT(s)                                #
    #######################################################################
    def act(self, how: Act, *args) -> None:
        print("how", how, args)
        gateway = {
            self.Act.OPEN: self.open,
            self.Act.CALL_OR_RAISE: self.cor,
            self.Act.DRAW: self.draw,
        }
        return gateway.get(how, "Error: how not found")(*args)

    # =====================
    # = Inner Caesar acts =
    # =====================
    def open(self, min_pot, c_bet, r_chips):
        # hand = (
        #    self.memorizer.rounds[self.memorizer.current_round]
        #    .opponents[self.name]
        #    .hand
        # )

        hand = self.hand
        print("c hand:", hand)
        # ========
        # = Odds =
        # ========
        odds = FB_cAction.describe(hand)
        print("!!current odds: ", odds)

        # ==========
        # = Policy =
        # ==========
        if odds["loss"] > 50:
            return AgentAction.CHECK
        if c_bet + r_chips < min_pot:
            return AgentAction.CHECK

        rdiff = r_chips - min_pot
        bet = int(np.interp(odds["win"], [0, 1], [0, rdiff]))

        return (AgentAction.OPEN, min_pot + bet)

    # =================
    # = Call or Raise =
    # =================
    def cor(self, max_bet, min_raise, c_bet, r_chips):
        # hand = (
        #    self.memorizer.rounds[self.memorizer.current_round]
        #    .opponents[self.name]
        #    .hand
        # )
        hand = self.hand
        print("c hand:", hand)

        # ========
        # = Odds =
        # ========
        odds = FB_cAction.describe(self.hand)
        print("!!current odds: ", odds)

        # ==========
        # = Policy =
        # ==========
        if odds["loss"] > 50:
            return AgentAction.FOLD
        if c_bet + r_chips > min_raise:
            return AgentAction.FOLD

        if odds["loss"] == 0:
            return AgentAction.ALLIN
        if odds["win"] < 70:
            return AgentAction.CALL

        if c_bet + r_chips > min_raise:
            return AgentAction.FOLD

        rdiff = r_chips - min_raise
        bet = int(np.interp(odds["win"], [0, 1], [0, rdiff]))

        return (AgentAction.RAISE, min_raise + bet)

    # ========
    # = Draw =
    # ========
    def draw(self, hand: list) -> str:
        print("given hand: ", hand)
        return " ".join(MC_CDraw.mc_ev_draw(hand=hand, M=300, max_depth=32)[1])
