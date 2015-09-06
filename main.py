import biography
import definitions

__author__ = 'willkydd'


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
    if phase == 2 and subphase == 0 and bio.canReachMinFinalAttributes() == True:
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
    if phase == 2 and subphase > 0:
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
            if bio.profRequirementsMet(pName):
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
                bio.skillBudget = definitions.professionbonusskilloffsets[prof]
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
            if bio.canIncreaseSkill(skl) and bio.skillBudget[skl] > 0:
                bio.path += "|+" + definitions.skills[skl][0]
                bio.skills[skl] += 1
                bio.EP -= bio.skillIncreaseCost(skl)
                bio.skillBudget[skl] -= 1
                explo(bio, phase, subphase + 1)
                explo(bio, phase + 1, 0)
                bio.skillBudget[skl] += 1
                bio.path = opath
                bio.skills[skl] -= 1
                bio.EP = oEP


setupMisc()
bio = biography.Biography()
explo(bio, 0, 0)
