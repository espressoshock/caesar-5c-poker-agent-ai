#######################################################################
#                     Client->Server Driver class                     #
#######################################################################


# = Imports

###################
#  Inject Caesar  #
###################
from caesar import Caesar

agent = Caesar()


# Agent
CURRENT_HAND = []


class PokerGames:
    def __init__(self):
        self.PlayerName = agent.name
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
    return _name


#################
#  Open Action  #
#################
# Called during open phase
def queryOpenAction(_minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
    pass


################
#  Call-Raise  #
################
# Called during bet call/raise phase
def queryCallRaiseAction(
    _maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips
):
    pass


##########
#  Draw  #
##########
# Called during draw phase
def queryCardsToThrow(_hand):
    pass


#######################################################################
#                             Info Utils                              #
#######################################################################


###############
#  New Round  #
###############
def infoNewRound(_round):
    print("new round", _round)
    pass


##############
#  Gameover  #
##############
def infoGameOver():
    pass


#################
#  Agent Chips  #
#################
def infoPlayerChips(_playerName, _chips):
    pass


#################
#  AnteChanged  #
#################
def infoAnteChanged(_ante):
    pass


###############
#  ForcedBet  #
###############
def infoForcedBet(_playerName, _forcedBet):
    pass


#############################
#  AgentOpenedBettingRound  #
#############################
def infoPlayerOpen(_playerName, _openBet):
    pass


##################
#  AgentChecked  #
##################
def infoPlayerCheck(_playerName):
    pass


#################
#  AgentRaised  #
#################
def infoPlayerRise(_playerName, _amountRaisedTo):
    pass


#################
#  AgentCalled  #
#################
def infoPlayerCall(_playerName):
    pass


#################
#  AgentFolded  #
#################
def infoPlayerFold(_playerName):
    pass


#################
#  Agent Allin  #
#################
def infoPlayerAllIn(_playerName, _allInChipCount):
    pass


###############
#  AgentDraw  #
###############
def infoPlayerDraw(_playerName, _cardCount):
    pass


####################
#  PlayerShowHand  #
####################
# called during showdown
def infoPlayerHand(_playerName, _hand):
    pass


###################
#  UndisputedWin  #
###################
# called during showdown
def infoRoundUndisputedWin(_playerName, _winAmount):
    pass


######################
#  AgentWinReported  #
######################
# called during showdown
def infoRoundResult(_playerName, _winAmount):
    pass
