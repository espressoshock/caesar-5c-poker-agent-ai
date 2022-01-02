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
    import random

    # Random action
    # replace me
    def chooseOpenOrCheck():
        if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
            # return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
            return (
                AgentAction.OPEN,
                (random.randint(0, 10) + _minimumPotAfterOpen)
                if _playersCurrentBet + _playersRemainingChips + 10
                > _minimumPotAfterOpen
                else _minimumPotAfterOpen,
            )
        else:
            return AgentAction.CHECK

    return {0: AgentAction.CHECK, 1: AgentAction.CHECK}.get(
        random.randint(0, 2), chooseOpenOrCheck()
    )


################
#  Call-Raise  #
################
# Called during bet call/raise phase
def queryCallRaiseAction(
    _maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips
):
    import random

    # random actino replace me
    def chooseRaiseOrFold():
        if _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
            return (
                AgentAction.RAISE,
                (random.randint(0, 10) + _minimumAmountToRaiseTo)
                if _playersCurrentBet + _playersRemainingChips + 10
                > _minimumAmountToRaiseTo
                else _minimumAmountToRaiseTo,
            )
        else:
            return AgentAction.FOLD

    return {
        0: AgentAction.FOLD,
        # 1: ClientBase.BettingAnswer.ACTION_ALLIN,
        1: AgentAction.FOLD,
        2: AgentAction.CALL
        if _playersCurrentBet + _playersRemainingChips > _maximumBet
        else AgentAction.FOLD,
    }.get(random.randint(0, 3), chooseRaiseOrFold())


##########
#  Draw  #
##########
# Called during draw phase
def queryCardsToThrow(_hand):
    # random replace me
    import random

    return _hand[random.randint(0, 4)] + " "


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
