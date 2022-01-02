#######################################################################
#                   Action Class | Memorizer Module                   #
#######################################################################

# Imports
import enum

#################
#  Action type  #
#################
class Type(enum.Enum):
    FORCED_BET = (0,)
    PLAYER_OPEN = (1,)
    PLAYER_CHECK = (2,)
    PLAYER_RAISE = (3,)
    PLAYER_CALL = (4,)
    PLAYER_FOLD = (5,)
    PLAYER_ALL_IN = (6,)
    PLAYER_DRAW = (7,)


class Action:
    #################
    #  Constructor  #
    #################
    def __init__(self, type: Type, *args):
        self.type = type
        self.values = args
        print("action: ", self.type, self.values)
