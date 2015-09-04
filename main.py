import biography
import definitions

__author__ = 'willkydd'


def explo(bio, phase, subphase):
    # print(str(phase)+"/"+str(subphase))
    if phase >= 3 + definitions.MAX_PROFS or bio.age >= definitions.MAX_AGE:
        if bio.EP == 0:
            print(bio.toCSV())
        return
    if phase == 0:
        # birth
        bio.path = "birth"
        # print(bio.toCSV())
        explo(bio, phase + 1, 0)
    if phase == 1:
        # picking sex
        opath = bio.path
        for sex in range(0, len(definitions.sexes)):
            bio.path = opath + "|" + definitions.sexes[sex]
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] += definitions.sexattributeoffsets[sex][i]
            bio.age += 0
            bio.sex = sex
            # print(bio.toCSV())
            explo(bio, phase + 1, 0)
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] -= definitions.sexattributeoffsets[sex][i]
            bio.age -= 0
            bio.path = opath
            bio.sex = -1
    if phase == 2 and subphase == 0:
        # picking a childhood
        opath = bio.path
        for childhood in range(0, len(definitions.childhoods)):
            bio.path = opath + "|" + definitions.childhoods[childhood]
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] += definitions.childhoodattributeoffsets[childhood][i]
            for i in range(0, len(definitions.skills)):
                bio.skills[i] += definitions.childhoodskilloffsets[childhood][i]
            bio.EP += definitions.childhoodepoffsets[childhood]
            bio.age += 15
            bio.childhood = childhood
            # print(bio.toCSV())
            explo(bio, phase, subphase + 1)
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] -= definitions.childhoodattributeoffsets[childhood][i]
            for i in range(0, len(definitions.skills)):
                bio.skills[i] -= definitions.childhoodskilloffsets[childhood][i]
            bio.EP -= definitions.childhoodepoffsets[childhood]
            bio.age -= 15
            bio.path = opath
            bio.childhood = -1
    if phase == 2 and subphase > 0 and not bio.failChildHoodMinAttributes():
        # pick way to distribute childhood ep to attributes
        opath = bio.path
        oEP = bio.EP
        minAttr = bio.getLastAttributeIncreased()
        if minAttr == -1:
            minAttr = 0
        for attr in range(minAttr, len(definitions.attributes)):
            if bio.canIncreaseAttribute(attr):
                bio.path = bio.path + "|+" + definitions.attributes[attr][0]
                bio.attributes[attr] += 1
                bio.EP -= bio.attributeIncreaseCost(attr)
                explo(bio, phase, subphase + 1)
                bio.path = opath
                bio.attributes[attr] -= 1
                bio.EP = oEP
        if bio.EP == 0:
            explo(bio, phase + 1, 0)
    if phase >= 3 and subphase == 0:
        # general occupation phase rules
        # AGE 15 OCCUPATlON BONUS: During a character's first occupation (at age 15-20), he or she gets an automatic +2 in every skill. In addition, the character gets an extra 20 EPs.
        if bio.age == 15:
            for i in range(0, len(definitions.skills)):
                bio.skills[i] += 2
            bio.EP += 20
        # AGE 20 OCCUPATION BONUS: At age 20 a character gets an extra 5EPs regardless of occupation chosen.
        if bio.age == 20:
            bio.EP += 5
        # AGING PENALTIES: At age 30 and beyond, if a character goes into another occupation rather than beginning to adventure, he or she will suffer some attribute penalties
        if bio.age >= 30:
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] += definitions.agingattributepenalities[bio.age][i]
        # start checking for each occupation's requirements being met or not
        oage = bio.age
        opath = bio.path
        oEP = bio.EP
        # pick occupation
        for prof in range(0, len(definitions.professions)):
            # some code here to test for profession requirements being met
            pName = definitions.professions[prof]
            # todo needs more conditions here
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
                    (pName == "Manorial Lord" and not (bio.getLastProfession() == "Manorial Lord" or (
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
                    (not pName in ["Recruit", "Veteran", "Soldier"]):
                profReqMet = False
            else:
                profReqMet = True

            if profReqMet:
                bio.path += "|" + definitions.professions[prof]
            bio.age += 5
            for i in range(0, len(definitions.attributes)):
                # Str and End do not receive occupation increases or decreases after the age of 40
                if bio.age - 5 <= 40 or (
                                definitions.attributes[i][0] != "Str" and definitions.attributes[i][0] != "End"):
                    bio.attributes[i] += definitions.professionattributeoffsets[prof][i]
            for i in range(0, len(definitions.skills)):
                bio.skills[i] += definitions.professionskilloffsets[prof][i]
            bio.EP += definitions.professionepoffsets[prof]
            bio.occupations.append(prof)
            explo(bio, phase, subphase + 1)
            bio.occupations.pop()
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] -= definitions.professionattributeoffsets[prof][i]
            for i in range(0, len(definitions.skills)):
                bio.skills[i] -= definitions.professionskilloffsets[prof][i]
            bio.EP = oEP
            bio.age = oage
            bio.path = opath
            # todo check that only x skillups are allowed for each profession
    if phase >= 3 and subphase > 0:
        # assign points to skills (attributes are fixed)
        opath = bio.path
        oEP = bio.EP
        minSkill = bio.getLastSkillIncreased()
        if minSkill == -1:
            minSkill = 0
        for skl in range(minSkill, len(definitions.skills)):
            if bio.canIncreaseSkill(skl):
                bio.path += "|+" + definitions.skills[skl][0]
                bio.skills[skl] += 1
                bio.EP -= bio.skillIncreaseCost(skl)
                explo(bio, phase, subphase + 1)
                explo(bio, phase + 1, 0)
                bio.path = opath
                bio.skills[skl] -= 1
                bio.EP = oEP


bio = biography.Biography()
header = "age, ep"
for i in range(0, len(definitions.attributes)):
    header += ", " + definitions.attributes[i][0]
for i in range(0, len(definitions.skills)):
    header += ", " + definitions.skills[i][0]
header += ", path"
print(header)
explo(bio, 0, 0)
