__author__ = 'willkydd'
import definitions


class Biography:
    attributes = [0] * definitions.attributeCount
    skills = [0] * definitions.skillCount
    age = 0
    path = ""
    EP = 0
    childhood = -1
    sex = -1
    occupations = []


    def toCSV(self):
        return str(self.age) + ", " + str(self.EP) + ", " + \
               str(self.attributes).strip("[]") + ", " + str(self.skills).strip("[]") + ", " + str(self.path)

    def canIncreaseAttribute(self, attributeNo):
        # children cannot increase attributes over 40
        if self.attributes[attributeNo] >= 40 and self.age == 15:
            return False

        # up to 30 1 point per, 30 to 39 2 points per and 40 costs 3 points
        if self.attributes[attributeNo] < 30:
            epcost = 1
        else:
            if self.attributes[attributeNo] < 40:
                epcost = 2
            else:
                epcost = 3
        if self.EP >= epcost:
            return True
        else:
            return False

    def attributeIncreaseCost(self, attributeNo):
        if self.attributes[attributeNo] < 30:
            return 1
        else:
            if self.attributes[attributeNo] < 40:
                return 2
            else:
                return 3

    def getLastAttributeIncreased(self):
        switcher = {"End": 0, "Str": 1, "Agi": 2, "Per": 3, "Int": 4, "Chr": 5}
        s = self.path.split("|").pop()
        if s[0] == "+":
            return switcher.get(s.split("+")[1])
        else:
            return -1
