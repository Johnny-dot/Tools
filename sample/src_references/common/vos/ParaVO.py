class ParaVO:
    def __init__(self) -> None:
        self._voDict ={}

    def getVal(self, key):
        return self._voDict[key]

    def setVal(self, key, val):
        self._voDict[key] = val

    def getAll(self):
        return self._voDict

    def getVal_Lua(self, key):
        value = self.getVal(key)
        if value is True or value is False:
            value = 'true' if value else 'false'

        return value

    def getVal_Python(self, key):
        value = self.getVal(key)
        if value == 'true' or value == 'false':
            value = True if value=='true' else False

        return value

    def setUniqueKey(self, key):
        self._uniqueKey = key
    def getUniqueKey(self):
        return self._uniqueKey

    def setFuncOutPath(self, path):
        self._funcOutPath = path

    def getFuncOutPath(self):
        return self._funcOutPath