__author__ = 'willkydd'
import sys

import definitions


class Biography:
    attributes = []
    skills = []
    age = None
    path = None
    EP = None
    childhood = None
    sex = None
    occupations = []
    skillBudget = []

    def __init__(self):
        self.attributes = [0] * len(definitions.attributes)
        self.skills = [0] * len(definitions.skills)
        self.age = 0
        self.path = ""
        self.EP = 0
        self.childhood = -1
        self.sex = -1
        self.occupations = []
        self.skillBudget = []

    def toCSV(self):
        return self.shrinkPath() + "," + str(self.age) + ", " + str(self.EP) + ", " + \
               str(self.attributes).strip("[]") + ", " + str(self.skills).strip("[]")

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
        if self.path[-4] == "+":
            lai = self.path[-3] + self.path[-2] + self.path[-1]
            for i in range(0, len(definitions.attributes)):
                if definitions.attributes[i][0] == lai:
                    return i
        else:
            return -1
        print("getlastattribute error")

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
        if self.age < 15:
            return True
        # todo Take aging penalties and STR/EN not taking bonuses after 40 into account
        # the number of attribute points needed to reach the targets
        attrDeficit = [0] * len(definitions.attributes)
        for i in range(0, len(definitions.attributes)):
            attrDeficit[i] = definitions.FINAL_ATTR_FLOORS[i] - self.attributes[i]
        # number of professions already taken
        numProfsTaken = int((max(self.age, 15) - 15) / 5)
        # the number of attribute points that can still be gained
        gainableAttributes = [0] * len(definitions.attributes)
        for i in range(0, len(definitions.attributes)):
            gainableAttributes[i] += definitions.maximumProfessionAttributeOffset[i] * (
                definitions.MAX_PROFS - numProfsTaken)
        if self.age == 15:
            for i in range(0, len(definitions.attributes)):
                gainableAttributes[i] += self.EP
        for i in range(0, len(definitions.attributes)):
            if gainableAttributes[i] < attrDeficit[i]:
                definitions.skipCounter += 1
                if definitions.skipCounter == definitions.skipInterval:
                    definitions.skipCounter = 0
                    sys.stderr.write(
                        self.toCSV() + " REJECTED because " + definitions.attributes[i][0] + " cannot reach " + str(
                            definitions.FINAL_ATTR_FLOORS[i]) + " from " + str(
                            self.attributes[i]) + " with only " + str(
                            gainableAttributes[i]) + " points still gainable.\n")
                return False
        return True

    def canReachMinFinalSkills(self):
        if self.age < 15:
            return True
        # the number of skill points needed to reach the targets
        sklDeficit = [0] * len(definitions.skills)
        for i in range(0, len(definitions.skills)):
            sklDeficit[i] = definitions.FINAL_SKILL_FLOORS.get(definitions.skills[i][0]) - self.skills[i]
        # number of professions already taken
        numProfsTaken = int((max(self.age, 15) - 15) / 5)
        # number of skill points that can still be gained
        gainableFreeSkills = [0] * len(definitions.skills)
        gainableEPSkills = [0] * len(definitions.skills)
        gainableEP = definitions.maximumEPOffset * (definitions.MAX_PROFS - numProfsTaken)
        for i in range(0, len(definitions.skills)):
            gainableFreeSkills[i] += definitions.maximumProfessionSkillOffsets[i] * (
                definitions.MAX_PROFS - numProfsTaken)
            gainableEPSkills[i] += definitions.maximumProfessionSkillBonusOffsets[i] * (
                definitions.MAX_PROFS - numProfsTaken)
        for i in range(0, len(definitions.skills)):
            if sklDeficit[i] > gainableFreeSkills[i] + max(gainableEPSkills[i], gainableEP):
                definitions.skipCounter += 1
                if definitions.skipCounter == definitions.skipInterval:
                    definitions.skipCounter = 0
                    sys.stderr.write(
                        self.toCSV() + " REJECTED because " + definitions.skills[i][0] + " cannot reach " + str(
                            definitions.FINAL_SKILL_FLOORS.get(i)) + " from " + str(
                            self.skills[i]) + " with only " + str(
                            gainableFreeSkills[i] + max(gainableEPSkills[i], gainableEP)) + " points still gainable.\n")
                return False
        return True

    def profRequirementsMet(self, profession):
        pName = profession
        bio = self

        if (pName == "Recruit" and not (bio.age <= 30 and not "Recruit" in bio.path)) or \
                (pName == "Soldier" and not bio.hasExperienceAsAnyOf(
                    ["Recruit", "Soldier", "Veteran", "Captain", "Knight", "Village Schulz", "Bandit"])) or \
                (pName == "Veteran" and not bio.hasExperienceAsAnyOf(
                    ["Soldier", "Veteran", "Captain", "Knights"])) or \
                (pName == "Captain" and not (
                        (bio.getAttribute("Per") >= 20 and bio.getAttribute(
                            "Int") >= 20 and bio.getAttribute(
                            "Chr") >= 20 and bio.hasExperienceAsAnyOf(
                            ["Veteran", "Captain", "Knight", "Village Schulz", "Courtier", "Manorial Lord",
                             "Bishop"])))) or \
                (pName == "Hunter" and not (bio.getSkill("WdWs") >= 15 and ((bio.age == 15 and (
                                    "Noble" in bio.path or "Country Crafts" in bio.path or "Country Commoners" in bio.path)) or bio.hasExperienceAsAnyOf(
                    ["Recruit", "Soldier", "Veteran", "Captain", "Knight", "Friar", "Hermit", "Peddler",
                     "Travelling Merchant", "Peasant", "Village Schulz", "Hunter", "Bandit"])))) or \
                (pName == "Bandit" and not (bio.age == 15 or bio.hasExperienceAsAnyOf(
                    ["Recruit", "Soldier", "Veteran", "Captain", "Knights", "Peasant", "Hunter", "Friar", "Hermit",
                     "Village Schulz", "Peddler", "Laborer", "Thief", "Bandit", "Vagabond", "Swindler"]))) or \
                (pName == "Peasant" and (
                                (bio.age == 15 and (
                                                "Nobility" in bio.path or "Wealthy Urban" in bio.path)) or bio.lastProfessionIn(
                                ["Captain", "Knight", "Courtier", "Noble Heir", "Priest", "Journeyman Craftsman",
                                 "Travelling Merchant", "Professor", "Alchemist"]) or bio.hasExperienceAsAnyOf(
                            ["Manorial Lord", "Abbot", "Bishop", "Merchant Proprietor", "Master Alchemist",
                             "Master Craftsman"]))) or \
                (pName == "Village Schulz" and not (
                            bio.hasExperienceAsAnyOf(["Peasant"]) and bio.hasExperienceAsAnyOf(
                            ["Veteran", "Captain", "Noble Heir", "Knight", "Manorial Lord", "Priest", "Abbot",
                             "Bishop",
                             "Merchant Proprietor", "Professor", "Village Schulz"]))) or \
                (pName == "Noble Heir" and not ("Nobility" in bio.path or "Courtier" in bio.path)) or \
                (pName == "Courtier" and not (
                                bio.lastProfessionIn(["Village Schulz",
                                                      "Captain", "Knight",
                                                      "Priest", "Abbot",
                                                      "Bishop"]) or bio.hasExperienceAsAnyOf(
                                ["Manorial Lord", "Courtier"]) or (bio.age == 15 and "Nobility" in bio.path))) or \
                (pName == "Knight" and not (bio.getSkill("Virt") >= 16 and (
                                bio.hasExperienceAsAnyOf(["Manorial Lord", "Knight"]) or bio.lastProfessionIn(
                                ["Captain", "Courtier", "Noble Heir", "Abbot", "Bishop"]) or (
                                        "Nobility" in bio.path and bio.age >= 20)))) or \
                (pName == "Manorial Lord" and not (bio.getLastProfession(1) == "Manorial Lord" or (
                            bio.prevProfessionIn(["Noble Heir", "Courtier", "Abbot", "Bishop"],
                                                 1) and bio.prevProfessionIn(
                            ["Noble Heir", "Courtier", "Abbot", "Bishop"], 2)))) or \
                (pName == "Hermit" and not bio.getSkill("Virt") >= 15) or \
                (pName == "Novice Monk/Nun" and not (
                            not "Novice Monk/Nun" in bio.path and not (
                                                    bio.getAttribute("Per") >= 15 and bio.getAttribute(
                                                "Int") >= 15 and bio.getAttribute("Chr") >= 15 and bio.getSkill(
                                        "Relg") >= 5 and bio.hasExperienceAsAnyOf(
                                    ["Noble Heir", "Courtier", "Manorial Lord", "Novice Mon/Nun", "Monk/Nun",
                                     "Friar",
                                     "Priest",
                                     "Abbot", "Bishop", "Student", "Clerk", "Physician", "Professor",
                                     "Alchemist"])))) or \
                (pName == "Monk/Nun" and not (bio.getAttribute("Per") >= 15 and bio.getAttribute(
                    "Int") >= 15 and bio.getAttribute("Chr") >= 15 and bio.getSkill(
                    "Relg") >= 5 and bio.hasExperienceAsAnyOf(
                    ["Noble Heir", "Courtier", "Manorial Lord", "Novice Mon/Nun", "Monk/Nun", "Friar", "Priest",
                     "Abbot", "Bishop", "Student", "Clerk", "Physician", "Professor", "Alchemist"]))) or \
                (pName == "Friar" and not ("male" in bio.path and bio.hasExperienceAsAnyOf(
                    ["Hermit", "Novice Monk/Nun", "Monk/Nun", "Priest", "Abbot", "Bishop"]))) or \
                (pName == "Priest" and not (
                                            "male" in bio.path and bio.getAttribute(
                                        "Per") >= 20 and bio.getAttribute(
                                    "Int") >= 20 and bio.getAttribute("Chr") >= 20 and (bio.hasExperienceAsAnyOf(
                            ["Manorial Lord", "Priest", "Abbot", "Bishop"]) or bio.lastProfessionIn(
                            ["Noble Heir", "Courtier", "Village Schulz", "Monk/Nun", "Clerk", "Professor"]) or (
                                    bio.prevProfessionIn(["Novice Monk/Nun", "Oblate", "Student", "Friar"],
                                                         2) and bio.prevProfessionIn(
                                    ["Novice Monk/Nun", "Oblate", "Student", "Friar"], 1))))) or \
                (pName == "Abbot" and not (bio.getAttribute("Per") >= 20 and bio.getAttribute(
                    "Int") >= 20 and bio.getAttribute("Chr") >= 20 and bio.getSkill("Relg") >= 15 and (
                            bio.lastProfessionIn(
                                ["Noble Heir", "Courtier", "Manorial Lord", "Priest", "Abbot", "Bishop"]) or (
                                    bio.prevProfessionIn(["Monk/Nun", "Professor"], 1) and bio.prevProfessionIn(
                                    ["Monk/Nun", "Professor"], 2))))) or \
                (pName == "Bishop" and not (bio.getAttribute("Per") >= 25 and bio.getAttribute(
                    "Int") >= 25 and bio.getAttribute("Chr") >= 25 and (
                            bio.lastProfessionIn(["Abbot", "Bishop"]) or (
                                    bio.prevProfessionIn(["Courtier", "Manorial Lord", "Priest"],
                                                         1) and bio.prevProfessionIn(
                                    ["Courtier", "Manorial Lord", "Priest"], 2))))) or \
                (pName == "Oblate" and (bio.getAttribute("Int") <= 11 or (bio.age == 15 and (
                                "Urban Commoners" in bio.path or "Country Commoners" in bio.path)) or bio.hasExperienceAsAnyOf(
                    ["Novice Monk/Nun", "Monk/Nun", "Friar", "Priest", "Abbot", "Bishop", "Clerk", "Professor",
                     "Physician", "Alchemist"]))) or \
                (pName == "Student" and not (bio.age == 15 or (bio.getAttribute("Int") >= 12 and bio.getSkill(
                    "R&Wr") >= 6 and bio.lastProfessionIn(
                    ["Recruit", "Soldier", "Veteran", "Hermit", "Apprentice Craftsman", "Journeyman Craftsman",
                     "Noble Heir", "Swindler", "Student"])))) or \
                (pName == "Clerk" and not ((bio.age == 15 and "Urban Commoners" in bio.path) or (
                                    bio.getAttribute("Int") >= 12 and bio.getSkill("R&Wr") >= 15 and (
                                    bio.hasExperienceAsAnyOf(
                                        ["Noble Heir", "Courtier", "Captain", "Knight", "Village Schulz", "Priest",
                                         "Abbot",
                                         "Bishop", "Student", "Clerk", "Professor", "Alchemist", "Master Alchemist",
                                         "Merchant Proprietor"]) or (
                                            bio.prevProfessionIn(["Oblate", "Monk", "Travelling Merchant"],
                                                                 1) and bio.prevProfessionIn(
                                            ["Oblate", "Monk", "Travelling Merchant"], 2)))))) or \
                (pName == "Physician" and not (bio.getSkill("Heal") >= 15 and bio.hasExperienceAsAnyOf(
                    ["Student", "Clerk", "Professor", "Physician", "Alchemist", "Master Alchemist"]))) or \
                (pName == "Professor" and not (bio.getSkill("R&Wr") >= 20 and bio.hasExperienceAsAnyOf(
                    ["Abbot", "Bishop", "Clerk", "Professor", "Physician", "Alchemist", "Mater Alchemist"]))) or \
                (pName == "Alchemist" and not (bio.getAttribute("Int") >= 30 and (bio.hasExperienceAsAnyOf(
                    ["Priest", "Abbot", "Bishop", "Student", "Clerk", "Professor", "Alchemist"]) or (
                            bio.prevProfessionIn(["Oblate", "Monk/Nun", "Friar", "Physician"],
                                                 1) and bio.prevProfessionIn(
                            ["Oblate", "Monk/Nun", "Friar", "Physician"], 2))))) or \
                (pName == "Master Alchemist" and not (bio.getAttribute("Int") > 35 and bio.hasExperienceAsAnyOf(
                    ["Alchemist"]))) or \
                (pName == "Vagabond" and (bio.lastProfessionIn(
                    ["Captain", "Knight", "Noble Heir", "Courtier", "Village Schulz", "Priest", "Professor",
                     "Travelling Merchant", "Alchemist"]) or bio.hasExperienceAsAnyOf(
                    ["Manorial Lord", "Abbot", "Bishop", "Merchant Proprietor", "Master Alchemist",
                     "Journeyman Craftsman", "Master Craftsman"]))) or \
                (pName == "Peddler" and not (("Commoner" in bio.path or bio.age > 15) and not ((
                            bio.lastProfessionIn(
                                ["Captain",
                                 "Knight",
                                 "Noble Heir",
                                 "Courtier",
                                 "Priest",
                                 "Professor",
                                 "Travelling Merchant",
                                 "Alchemist"]) or bio.hasExperienceAsAnyOf(
                            ["Manorial Lord",
                             "Abbot",
                             "Bishop",
                             "Merchant Proprietor",
                             "Master Alchemist",
                             "Journeyman Craftsman",
                             "Master Craftsman",
                             "Village Schulz"]))))) or \
                (pName == "Local Trader" and not ((bio.age == 15 and (
                                    "Nobility" in bio.path or "Wealthy Urban" in bio.path or "Country Crafts" in bio.path)) or (
                                    bio.getAttribute("Int") >= 12 and bio.getSkill(
                                "SpkC") >= 5 and bio.hasExperienceAsAnyOf(
                            ["Captain", "Noble Heir", "Courtier", "Monk/Nun", "Priest", "Abbot", "Bishop", "Clerk",
                             "Physician", "Professor", "Alchemist", "Journeyman Craftsman", "Master Craftsman",
                             "Swindler",
                             "Peddler", "Local Trader", "Travelling Merchant", "Merchant Proprietor"])))) or \
                (pName == "Travelling Merchant" and not (
                            (bio.age == 15 and ("Nobility" in bio.path or "Wealthy Urban" in bio.path)) or (
                                            bio.getAttribute("Int") >= 15 and bio.getSkill(
                                        "SpkC") >= 20 and bio.hasExperienceAsAnyOf(
                                    ["Local Trader", "Travelling Merchant", "Merchant Proprietor", "Noble Heir",
                                     "Manorial Lord",
                                     "Professor", "Master Alchemist", "Master Craftsman"])))) or \
                (pName == "Merchant Proprietor" and not (
                                    bio.getAttribute("Int") >= 20 and bio.getSkill(
                                "SpkC") >= 10 and bio.lastProfessionIn(
                            ["Travelling Merchant", "Merchant Proprietor", "Manorial Lord", "Bishop"]))) or \
                (pName == "Laborer" and ((bio.age == 15 and "Nobility in bio.path") or bio.lastProfessionIn(
                    ["Captain", "Knight", "Noble Heir", "Courtier", "Village Schulz", "Priest", "Professor",
                     "Alchemist", "Travelling Merchant"]) or bio.hasExperienceAsAnyOf(
                    ["Manorial Lord", "Abbot", "Bishop", "Merchant Proprietor", "Master Alchemist",
                     "Master Craftsman"]))) or \
                (pName == "Apprentice Craftsman" and not ("Apprentice Craftsman" not in bio.path and (
                                (bio.age == 15 and "Nobility" not in bio.path) or bio.lastProfessionIn(
                                ["Captain", "Knight", "Noble Heir", "Courtier", "Village Schulz", "Priest", "Clerk",
                                 "Physician", "Professor", "Alchemist",
                                 "Travelling Merchant"]) or bio.hasExperienceAsAnyOf(
                            ["Manorial Lord", "Abbot", "Bishop", "Merchant Proprietor", "Master Alchemist",
                             "Journeyman Craftsman", "Master Craftsman"])))) or \
                (pName == "Journeyman Craftsman" and not ((bio.age == 15 and (
                                "Town Trades" in bio.path or "Country Crafts" in bio.path)) or bio.hasExperienceAsAnyOf(
                    ["Apprentice Craftsman", "Journeyman Craftsman", "Master Craftsman", "Physician",
                     "Alchemist"]))) or \
                (pName == "Master Craftsman" and not (bio.getAttribute("Int") >= 12 and bio.hasExperienceAsAnyOf(
                    ["Journeyman Craftsman", "Master Craftsman", "Merchant Proprietor"]))) or \
                (pName == "Thief" and not ((
                                                               bio.age == 15 and "Country Crafts" not in bio.path and "Country Commoners" not in bio.path) or (
                                bio.getSkill("StrW") >= 10 and bio.hasExperienceAsAnyOf(
                            ["Soldier", "Veteran", "Priest", "Friar", "Hunter", "Bandit", "Thief", "Vagabond",
                             "Laborer",
                             "Peddler", "Local Trader", "Travelling Merchant", "Student", "Clerk", "Professor",
                             "Alchemist",
                             "Journeyman Craftsman"])))) or \
                (pName == "Swindler" and not ((bio.age == 15 and (
                                    "Nobility" in bio.path or "Wealthy Urban" in bio.path or "Town Trades" in bio.path)) or (
                                    bio.getAttribute("Int") >= 25 and bio.getSkill(
                                "StrW") >= 15 and bio.hasExperienceAsAnyOf(
                            ["Soldier", "Veteran", "Priest", "Friar", "Hunter", "Bandit", "Thief", "Vagabond",
                             "Laborer",
                             "Peddler", "Local Trader", "Travelling Merchant", "Student", "Clerk", "Professor",
                             "Alchemist",
                             "Journeyman Craftsman"])))):
            return False
        else:
            return True
