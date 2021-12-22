######################################
#  Game-specific configs and Consts  #
######################################


class AgentAction:
    OPEN = "Open"
    CHECK = "Check"
    CALL = "Call"
    RAISE = "Raise"
    FOLD = "Fold"
    ALLIN = "All-in"


class Network:
    SERVER_TCP_IP = "172.28.16.1"
    SERVER_TCP_PORT = 5000
    BUFFER_SIZE = 1024
