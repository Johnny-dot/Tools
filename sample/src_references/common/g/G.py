_GUI = True

global GLOBALS_DICT
GLOBALS_DICT = {}

def setG(key, val):
    try:
        GLOBALS_DICT[key] = val
    except KeyError:
        pass

def getG(key):
    try:
        return GLOBALS_DICT[key]
    except KeyError:
        return "Not Found"