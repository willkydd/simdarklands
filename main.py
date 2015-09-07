import operator
import copy

import biography
import definitions

__author__ = 'willkydd'
prioattributes = list()

def setupMisc():
    header = "path, age, ep"
    for i in range(0, len(definitions.attributes)):
        header += ", " + definitions.attributes[i][0]
    for i in range(0, len(definitions.skills)):
        header += ", " + definitions.skills[i][0]
    print(header)
    # check which is the maximum possible attribute increase from one professional choice
    for i in range(0, len(definitions.attributes)):
        for j in range(0, len(definitions.professions)):
            if definitions.professionattributeoffsets[j][i] > definitions.maximumProfessionAttributeOffset[i]:
                definitions.maximumProfessionAttributeOffset[i] = definitions.professionattributeoffsets[j][i]
    # check which is the maximum possible skill increase from one professional choice
    for i in range(0, len(definitions.skills)):
        for j in range(0, len(definitions.professions)):
            if definitions.professionskilloffsets[j][i] > definitions.maximumProfessionSkillOffsets[i]:
                definitions.maximumProfessionSkillOffsets[i] = definitions.professionskilloffsets[j][i]
    # check which is the maximum possible skill increase from one professional choice
    for i in range(0, len(definitions.skills)):
        for j in range(0, len(definitions.professions)):
            if definitions.professionbonusskilloffsets[j][i] > definitions.maximumProfessionSkillBonusOffsets[i]:
                definitions.maximumProfessionSkillBonusOffsets[i] = definitions.professionbonusskilloffsets[j][i]
    # setup priorityattributes and skills based on how needed they are to reach targets
    for i in range(0, len(definitions.attributes)):
        prioattributes.append([definitions.attributes[i][0], definitions.FINAL_ATTR_FLOORS[i], i])
    prioattributes.sort(key=operator.itemgetter(1), reverse=True)
    print(prioattributes)
    # input("")

def explo(bio, phase, subphase):
    # print(str(phase)+"/"+str(subphase))
    if phase >= 3 + definitions.MAX_PROFS or bio.age >= definitions.MAX_AGE or not bio.canReachMinFinalAttributes() == True or not bio.canReachMinFinalSkills() == True:
        if bio.EP == 0 and (bio.age == definitions.MAX_AGE or len(bio.occupations) == definitions.MAX_PROFS):
            print(bio.toCSV())
            input("Found one")
        return
    if phase == 0:
        # birth
        bio.path = "birth"
        bio.age = 0
        bio.occupations.clear()
        explo(bio, phase + 1, 0)
    if phase == 1:
        # picking sex
        obio = copy.deepcopy(bio)
        for sex in range(0, len(definitions.sexes)):
            bio.path = obio.path + "|" + definitions.sexes[sex]
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] += definitions.sexattributeoffsets[sex][i]
            bio.sex = sex
            explo(bio, phase + 1, 0)
            bio = copy.deepcopy(obio)
    if phase == 2 and subphase == 0:
        # picking a childhood
        bio.age = 15
        obio = copy.deepcopy(bio)
        for ch in range(0, len(definitions.childhoods)):
            bio.childhood = ch
            bio.path = obio.path + "|" + definitions.childhoods[ch]
            for i in range(0, len(definitions.attributes)):
                bio.attributes[i] += definitions.childhoodattributeoffsets[ch][i]
            for i in range(0, len(definitions.skills)):
                bio.skills[i] += definitions.childhoodskilloffsets[ch][i]
            bio.EP += definitions.childhoodepoffsets[ch]
            explo(bio, phase, subphase + 1)
            bio = copy.deepcopy(obio)
    if phase == 2 and subphase > 0:
        # pick way to distribute childhood ep to attributes
        obio = copy.deepcopy(bio)
        minAttr = bio.getLastAttributeIncreased()
        if minAttr == -1:
            minAttr = 0
        prioMinAttr = 0
        for i in range(0, len(prioattributes)):
            if prioattributes[i][2] == minAttr:
                prioMinAttr = i
                break
        for prioAttr in range(prioMinAttr, len(prioattributes)):
            if bio.canIncreaseAttribute(prioattributes[prioAttr][2]):
                bio.path = bio.path + "|+" + prioattributes[prioAttr][0]
                bio.attributes[prioattributes[prioAttr][2]] += 1
                bio.EP -= bio.attributeIncreaseCost(prioattributes[prioAttr][2])
                explo(bio, phase, subphase + 1)
                bio = copy.deepcopy(obio)
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
        obio = copy.deepcopy(bio)
        # pick occupation
        for prof in range(0, len(definitions.professions)):
            pName = definitions.professions[prof]
            if bio.profRequirementsMet(pName):
                bio.path += "|" + pName
                bio.age += 5
                for i in range(0, len(definitions.attributes)):
                    # Str and End do not receive occupation increases or decreases after the age of 40
                    if bio.age - 5 <= 40 or (
                                    definitions.attributes[i][0] != "Str" and definitions.attributes[i][0] != "End"):
                        bio.attributes[i] += definitions.professionattributeoffsets[prof][i]
                for i in range(0, len(definitions.skills)):
                    bio.skills[i] += definitions.professionskilloffsets[prof][i]
                bio.EP = definitions.professionepoffsets[prof]
                bio.occupations.append(prof)
                bio.skillBudget = definitions.professionbonusskilloffsets[prof]
                explo(bio, phase, subphase + 1)
                bio = copy.deepcopy(obio)
    if phase >= 3 and subphase > 0:
        # assign points to skills (attributes are fixed)
        obio = copy.deepcopy(bio)
        minSkill = bio.getLastSkillIncreased()
        if minSkill == -1:
            minSkill = 0
        for skl in range(minSkill, len(definitions.skills)):
            if bio.canIncreaseSkill(skl) and bio.skillBudget[skl] > 0:
                bio.path += "|+" + definitions.skills[skl][0]
                bio.skills[skl] += 1
                bio.EP -= bio.skillIncreaseCost(skl)
                bio.skillBudget[skl] -= 1
                explo(bio, phase, subphase + 1)
                if bio.EP == 0:
                    explo(bio, phase + 1, 0)
                bio = copy.deepcopy(obio)


setupMisc()
bio = biography.Biography()
explo(bio, 0, 0)
