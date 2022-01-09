#######################################################################
#                     Client->Server Driver class                     #
#######################################################################


# = Imports

###################
#  Inject Caesar  #
###################
from caesar import Caesar
from game_config import AgentAction
from round import WinType


class PokerGame:
    # ==================
    # = Game specifics =
    # ==================
    n_players = 2  # make sure this is correct
    opponents = dict

    # ===============
    # = Plug Caesar =
    # ===============
    agent = Caesar(n_players=n_players)

    def __init__(self):
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0


#######################################################################
#                          Driver Connectors                          #
#######################################################################

################
#  Agent Name  #
################
# returns agent name
def queryPlayerName(_name: str) -> str:
    return PokerGame.agent.name


#################
#  Open Action  #
#################
# Called during open phase
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    print("---->:open invoked")
    return PokerGame.agent.act(
        Caesar.Act.OPEN,
        _minimumPotAfterOpen,
        _playersCurrentBet,
        _playersRemainingChips,
    )


################
#  Call-Raise  #
################
# Called during bet call/raise phase
def queryCallRaiseAction(
    _maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips
):
    print("---->:cor invoked")
    return PokerGame.agent.act(
        Caesar.Act.CALL_OR_RAISE,
        _maximumBet,
        _minimumAmountToRaiseTo,
        _playersCurrentBet,
        _playersRemainingChips,
    )


##########
#  Draw  #
##########
# Called during draw phase
def queryCardsToThrow(_hand):
    return PokerGame.agent.act(Caesar.Act.DRAW, _hand)


#######################################################################
#                             Info Utils                              #
#######################################################################


###############
#  New Round  #
###############
def infoNewRound(_round):
    PokerGame.agent.see(Caesar.See.NEW_ROUND, _round)
    pass


##############
#  Gameover  #
##############
def infoGameOver():
    PokerGame.agent.see(Caesar.See.GAME_OVER)
    pass


#################
#  Agent Chips  #
#################
def infoPlayerChips(_playerName, _chips):
    PokerGame.agent.see(Caesar.See.PLAYER_CHIPS, _playerName, _chips)


#################
#  AnteChanged  #
#################
def infoAnteChanged(_ante):
    PokerGame.agent.see(Caesar.See.ANTE_CHANGED, _ante)
    pass


###############
#  ForcedBet  #
###############
def infoForcedBet(_playerName, _forcedBet):
    PokerGame.agent.see(Caesar.See.FORCED_BET, _playerName, _forcedBet)
    pass


#############################
#  AgentOpenedBettingRound  #
#############################
def infoPlayerOpen(_playerName, _openBet):
    PokerGame.agent.see(Caesar.See.PLAYER_OPEN, _playerName, _openBet)
    pass


##################
#  AgentChecked  #
##################
def infoPlayerCheck(_playerName):
    PokerGame.agent.see(Caesar.See.PLAYER_CHECK, _playerName)
    pass


#################
#  AgentRaised  #
#################
def infoPlayerRise(_playerName, _amountRaisedTo):
    PokerGame.agent.see(Caesar.See.PLAYER_RAISE, _playerName, _amountRaisedTo)
    pass


#################
#  AgentCalled  #
#################
def infoPlayerCall(_playerName):
    PokerGame.agent.see(Caesar.See.PLAYER_CALL, _playerName)
    pass


#################
#  AgentFolded  #
#################
def infoPlayerFold(_playerName):
    PokerGame.agent.see(Caesar.See.PLAYER_FOLD, _playerName)
    pass


#################
#  Agent Allin  #
#################
def infoPlayerAllIn(_playerName, _allInChipCount):
    PokerGame.agent.see(Caesar.See.PLAYER_ALL_IN, _playerName, _allInChipCount)
    pass


###############
#  AgentDraw  #
###############
def infoPlayerDraw(_playerName, _cardCount):
    PokerGame.agent.see(Caesar.See.PLAYER_DRAW, _playerName, _cardCount)
    pass


####################
#  PlayerShowHand  #
####################
# called during showdown
def infoPlayerHand(_playerName, _hand):
    PokerGame.agent.see(Caesar.See.PLAYER_HAND, _playerName, _hand)
    pass


###################
#  UndisputedWin  #
###################
# called during showdown
def infoRoundUndisputedWin(_playerName, _winAmount):
    PokerGame.agent.see(
        Caesar.See.ROUND_OVER_UNDISPUTED, WinType.UNDISPUTED, _playerName, _winAmount
    )
    pass


######################
#  AgentWinReported  #
######################
# called during showdown
def infoRoundResult(_playerName, _winAmount):
    PokerGame.agent.see(
        Caesar.See.ROUND_OVER_DISPUTED, WinType.DISPUTED, _playerName, _winAmount
    )
    pass
