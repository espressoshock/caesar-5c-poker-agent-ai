#######################################################################
#                             Round Class                             #
#######################################################################

# Imports


class Round:
    ############
    #  Player  #
    ############
    class Player:
        def __init__(self, chips: int):
            self.chips = chips

    #################
    #  Constructor  #
    #################
    def __init__(self, ante: int, opponents: list):
        self._number = 0
        self._ante = ante
        self._opponents = {o.name: self.Player(o.chips) for o in opponents}
