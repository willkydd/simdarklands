__author__ = 'willkydd'
import definitions


class Biography:
    attributes = [0] * len(definitions.attributes)
    skills = [0] * len(definitions.skills)
    age = 0
    path = ""
    EP = 0
    childhood = -1
    sex = -1
    occupations = []

    def toCSV(self):
        return str(self.age) + ", " + str(self.EP) + ", " + \
               str(self.attributes).strip("[]") + ", " + str(self.skills).strip("[]") + ", " + self.shrinkPath()

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

    def skillIncreaseCost(self, skillNo):
        if self.skills[skillNo] < 50:
            return 1
        else:
            return 2

    def getLastAttributeIncreased(self):
        # switcher = {"End": 0, "Str": 1, "Agi": 2, "Per": 3, "Int": 4, "Chr": 5}
        switcher = {}
        for i in range(0, len(definitions.attributes)):
            switcher[definitions.attributes[i][0]] = i
        if self.path[-4] == "+":
            return switcher.get(self.path[-3] + self.path[-2] + self.path[-1])
        else:
            return -1

    def getLastSkillIncreased(self):
        switcher = {}
        for i in range(0, len(definitions.skills)):
            switcher[definitions.skills[i][0]] = i
        if self.path[-5] == "+":
            return switcher.get(self.path[-4] + self.path[-3] + self.path[-2] + self.path[-1])
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
        for i in range(0, len(definitions.CHILDHOOD_ATTR_FLOORS)):
            epNeeded += self.EPNeededToRaiseAttributeTo(i, definitions.CHILDHOOD_ATTR_FLOORS[i])
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

    def canIncreaseSkill(self, skillNo):
        return self.EP >= self.EPNeededToRaiseSkillTo(skillNo, self.skills[skillNo] + 1)

    def shrinkPath(self):
        result = ""
        ele = self.path.split("|")
        idx = 0
        while idx < len(ele):
            cnt = 1
            result += "|" + ele[idx]
            if idx + 1 < len(ele):
                while ele[idx] == ele[idx + 1]:
                    cnt += 1
                    idx += 1
                    if idx + 1 >= len(ele):
                        break
                if cnt > 1:
                    result += "x" + str(cnt)
            idx += 1
        return result

    def getAttribute(self, attr):
        return self.attributes[definitions.attributeindices[attr]]

    def getSkill(self, skl):
        return self.skills[definitions.skillindices[skl]]

    def hasExperienceAsAnyOf(self, professions):
        for i in range(0, len(professions)):
            if professions[i] in self.path:
                return True
        return False

    def getLastProfession(self):
        if len(self.occupations) == 0:
            return -1
        else:
            return self.occupations[-1]

    def lastProfessionIn(self, professions):
        if len(professions) == 0:
            return False
        lp = self.getLastProfession()
        if lp == -1:
            return False
        for i in range(0, len(professions)):
            if definitions.professionindices[professions[i]] == lp:
                return True
        return False
