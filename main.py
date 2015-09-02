__author__ = 'willkydd'

import biography
import definitions


def explo(bio, phase, subphase):
    if phase >= 5:
        return
    if phase == 0:
        # birth
        print("Initiating...")
        bio.path = "birth"
        print(bio.toCSV())
        explo(bio, phase + 1, 0)
    if phase == 1:
        # picking sex
        opath = bio.path
        for sex in range(0, len(definitions.Sexes)):
            bio.path = opath + "|" + definitions.Sexes[sex]
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] += definitions.sexAttributeOffsets[sex][i]
            bio.age += 0
            bio.sex = sex
            print(bio.toCSV())
            explo(bio, phase + 1, 0)
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] -= definitions.sexAttributeOffsets[sex][i]
            bio.age -= 0
            bio.path = opath
            bio.sex = -1
    if phase == 2 and subphase == 0:
        opath = bio.path
        for childhood in range(0, len(definitions.Childhoods)):
            bio.path = opath + "|" + definitions.Childhoods[childhood]
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] += definitions.childhoodAttributeOffsets[childhood][i]
            for i in range(0, definitions.skillCount):
                bio.skills[i] += definitions.childhoodSkillOffsets[childhood][i]
            bio.EP += definitions.childhoodEPOffsets[childhood]
            bio.age += 15
            bio.childhood = childhood
            print(bio.toCSV())
            explo(bio, phase, subphase + 1)
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] -= definitions.childhoodAttributeOffsets[childhood][i]
            for i in range(0, definitions.skillCount):
                bio.skills[i] -= definitions.childhoodSkillOffsets[childhood][i]
            bio.EP -= definitions.childhoodEPOffsets[childhood]
            bio.age -= 15
            bio.path = opath
            bio.childhood = -1
    if phase == 2 and subphase > 0:
        # pick way to distribute childhood ep to attributes
        opath = bio.path
        if bio.getLastAttributeIncreased() == -1:
            minAttr = 0
        else:
            minAttr = bio.getLastAttributeIncreased()
        for attr in range(minAttr, definitions.attributeCount):
            if bio.canIncreaseAttribute(attr):
                bio.path = bio.path + "|" + "+" + definitions.Attributes[attr][0]
                bio.attributes[attr] += 1
                bio.EP -= bio.attributeIncreaseCost(attr)
                explo(bio, phase, subphase + 1)
                bio.path = opath
                bio.attributes[attr] -= 1
                bio.EP += bio.attributeIncreaseCost(attr)
        if bio.EP == 0:
            explo(bio, phase + 1, 0)
    if phase >= 3 and subphase == 0:
        # pick occupation
        print(bio.toCSV())
    if phase >= 3 and subphase > 0:
        # assign points to skills (attributes are fixed)
        print(bio.toCSV())


bio = biography.Biography()
explo(bio, 0, 0)
