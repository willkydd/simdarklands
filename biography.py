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
    skillBudget = []

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
        if self.EP < self.EPNeededToRaiseSkillTo(skillNo, self.skills[skillNo] + 1):
            return False
        return True

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

    def getLastProfession(self, levels):
        if len(self.occupations) < levels:
            return -1
        else:
            return self.occupations[-levels]

    def lastProfessionIn(self, professions):
        if len(professions) == 0:
            return False
        lp = self.getLastProfession(1)
        if lp == -1:
            return False
        for i in range(0, len(professions)):
            if definitions.professionindices[professions[i]] == lp:
                return True
        return False

    def prevProfessionIn(self, professions, level):
        if len(professions) == 0:
            return False
        lp = self.getLastProfession(level)
        if lp == -1:
            return False
        for i in range(0, len(professions)):
            if definitions.professionindices[professions[i]] == lp:
                return True
        return False

    def canReachMinFinalAttributes(self):
        # todo Take aging penalties and STR/EN not taking bonuses after 40 into account
        # the number of attribute points needed to reach the targets
        attrDeficit = [0] * len(definitions.attributes)
        for i in range(0, len(definitions.attributes)):
            attrDeficit[i] = definitions.FINAL_ATTR_FLOORS[i] - self.attributes[i]
        # number of professions already taken
        numProfsTaken = int((max(self.age, 15) - 15) / 5)
        # the number of attribute points gainable
        gainableAttributes = [0] * len(definitions.attributes)
        for i in range(0, len(definitions.attributes)):
            gainableAttributes[i] += definitions.maximumProfessionAttributeOffset[i] * (
                definitions.MAX_PROFS - numProfsTaken)
        if self.age == 15:
            for i in range(0, len(definitions.attributes)):
                gainableAttributes[i] += self.EP
        if self.age < 15:
            return True
        for i in range(0, len(definitions.attributes)):
            if gainableAttributes[i] < attrDeficit[i]:
                print(self.toCSV() + " REJECTED because " + definitions.attributes[i][0] + " cannot reach " + str(
                    definitions.FINAL_ATTR_FLOORS[i]) + " from " + str(self.attributes[i]) + " with only " + str(
                    gainableAttributes[i]) + " points still gainable.")
                return False
        return True
