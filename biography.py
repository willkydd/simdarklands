__author__ = 'willkydd'
import definitions


class Biography:
    attributes = [0] * len(definitions.Attributes)
    skills = [0] * len(definitions.Skills)
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
        # switcher = {"End": 0, "Str": 1, "Agi": 2, "Per": 3, "Int": 4, "Chr": 5}
        switcher = {}
        for i in range(0, len(definitions.Attributes)):
            switcher[definitions.Attributes[i][0]] = i
        if self.path[-4] == "+":
            return switcher.get(self.path[-3] + self.path[-2] + self.path[-1])
        else:
            return -1

    def getLastSkillIncreased(self):
        switcher = {}
        for i in range(0, len(definitions.Skills)):
            switcher[definitions.Skills[i][0]] = i
        if self.path[-5] == "+":
            return switcher.get(self.path[-3] + self.path[-2] + self.path[-1])
        else:
            return -1

    def EPNeededToRaiseAttributeTo(self, attrNo, target):
        x = self.attributes[attrNo]
        y = target
        if x >= y:
            return 0
        else:
            return self.EPNeededToRaiseAttributeFrom1toX(y) - self.EPNeededToRaiseAttributeFrom1toX(x)

    def EPNeededToRaiseAttributeFrom1toX(self, x):
        retval = 0
        if x <= 29:
            retval = x
        if x > 29 and x <= 39:
            retval = 29 + (x - 29) * 2
        if x > 39:
            retval = 29 + 20 + (x - 39) * 3
        return retval

    def failChildHoodMinAttributes(self):
        epNeeded = 0
        for i in range(0, len(definitions.ChildHoodAttributeFloors)):
            epNeeded += self.EPNeededToRaiseAttributeTo(i, definitions.ChildHoodAttributeFloors[i])
            if self.EP < epNeeded:
                return True
        # if self.EP<epNeeded:
        #    print("aborting:")
        #    print(self.toCSV())
        return self.EP < epNeeded

    def EPNeededToRaiseSkillFrom1toX(self, x):
        retval = 0
        if x <= 49:
            retval = x
        if x > 49:
            retval = 49 + (x - 49) * 2
        return retval

    def EPNeededToRaiseSkillTo(self, skillNo, target):
        x = self.skills[skillNo]
        y = target
        if x >= y:
            return 0
        else:
            return self.EPNeededToRaiseSkillFrom1toX(y) - self.EPNeededToRaiseSkillFrom1toX(x)
