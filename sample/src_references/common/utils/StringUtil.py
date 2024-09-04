import Levenshtein
from fuzzywuzzy import fuzz

def PartialRatio(str1, str2, rate):
    return fuzz.partial_ratio(str1, str2) >= rate

def Py2LuaBool(para):
    if para == True:
        return 'true'
    elif para == False:
        return 'false'
    else:
        return para

def Lua2PyBool(para):
    if para == 'true' or para == True:
        return True
    elif para == 'false' or para == False:
        return False
    else:
        return para

def checkBool(para):
    if para == 'true':
        return True
    elif para == 'false':
        return False
    else:
        return para