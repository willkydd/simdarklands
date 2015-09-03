__author__ = 'willkydd'

import biography
import definitions


def explo(bio, phase, subphase):
    if phase >= 5:
        return
    if phase == 0:
        # birth
        bio.path = "birth"
        # print(bio.toCSV())
        explo(bio, phase + 1, 0)
    if phase == 1:
        # picking sex
        opath = bio.path
        for sex in range(0, len(definitions.Sexes)):
            bio.path = opath + "|" + definitions.Sexes[sex]
            for i in range(0, len(definitions.Attributes)):
                bio.attributes[i] += definitions.sexAttributeOffsets[sex][i]
            bio.age += 0
            bio.sex = sex
            # print(bio.toCSV())
            explo(bio, phase + 1, 0)
            for i in range(0, len(definitions.Attributes)):
                bio.attributes[i] -= definitions.sexAttributeOffsets[sex][i]
            bio.age -= 0
            bio.path = opath
            bio.sex = -1
    if phase == 2 and subphase == 0:
        # picking a childhood
        opath = bio.path
        for childhood in range(0, len(definitions.Childhoods)):
            bio.path = opath + "|" + definitions.Childhoods[childhood]
            for i in range(0, len(definitions.Attributes)):
                bio.attributes[i] += definitions.childhoodAttributeOffsets[childhood][i]
            for i in range(0, len(definitions.Skills)):
                bio.skills[i] += definitions.childhoodSkillOffsets[childhood][i]
            bio.EP += definitions.childhoodEPOffsets[childhood]
            bio.age += 15
            bio.childhood = childhood
            # print(bio.toCSV())
            explo(bio, phase, subphase + 1)
            for i in range(0, len(definitions.Attributes)):
                bio.attributes[i] -= definitions.childhoodAttributeOffsets[childhood][i]
            for i in range(0, len(definitions.Skills)):
                bio.skills[i] -= definitions.childhoodSkillOffsets[childhood][i]
            bio.EP -= definitions.childhoodEPOffsets[childhood]
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
        for attr in range(minAttr, len(definitions.Attributes)):
            if bio.canIncreaseAttribute(attr):
                bio.path = bio.path + "|" + "+" + definitions.Attributes[attr][0]
                bio.attributes[attr] += 1
                bio.EP -= bio.attributeIncreaseCost(attr)
                explo(bio, phase, subphase + 1)
                bio.path = opath
                bio.attributes[attr] -= 1
                bio.EP = oEP
        if bio.EP == 0:
            explo(bio, phase + 1, 0)
    if phase >= 3 and subphase == 0:
        # pick occupation
        print(bio.toCSV())
    if phase >= 3 and subphase > 0:
        # assign points to skills (attributes are fixed)
        print(bio.toCSV())


bio = biography.Biography()
header = "age, ep"
for i in range(0, len(definitions.Attributes)):
    header += ", " + definitions.Attributes[i][0]
for i in range(0, len(definitions.Skills)):
    header += ", " + definitions.Skills[i][0]
header += ", path"
print(header)
explo(bio, 0, 0)
