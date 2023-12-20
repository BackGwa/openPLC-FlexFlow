from random import randint

BOOL = "BOOL"
INT = "INT"
REAL = "REAL"


def MEMORY(DATA_TYPE, ADDRESS_MAIN, ADDRESS_SUB):
    return f"MEMORY/{DATA_TYPE}/{ADDRESS_MAIN}x{ADDRESS_SUB}"


def SESSION_ID(SESSION, MODULE):
    return f"FlexFlow_{SESSION}_{MODULE}_{randint(0, 65534)}"


def TOPIC(SESSION, MODULE, TOPIC):
    return f"flexflow/{SESSION}/{MODULE}/{TOPIC}"