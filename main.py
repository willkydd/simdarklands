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
        for sex in range(1, 3):
            bio.path = opath + "|" + definitions.sexList[sex]
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] += definitions.sexAttributes[sex][i]
            bio.age += 0
            print(bio.toCSV())
            explo(bio, phase + 1, 0)
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] -= definitions.sexAttributes[sex][i]
            bio.age -= 0
            bio.path = opath
    if phase == 2:
        opath = bio.path
        for childhood in range(0, len(definitions.childhoods)):
            bio.path = opath + "|" + definitions.childhoods[childhood]
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] += definitions.childhoodsAttributeOffsets[childhood][i]
            for i in range(0, definitions.skillCount):
                bio.skills[i] += definitions.childhoodsSkillOffsets[childhood][i]
            bio.EP += definitions.childhoodEPs[childhood]
            bio.age += 15
            print(bio.toCSV())
            explo(bio, phase + 1, 0)
            for i in range(0, definitions.attributeCount):
                bio.attributes[i] -= definitions.childhoodsAttributeOffsets[childhood][i]
            for i in range(0, definitions.skillCount):
                bio.skills[i] -= definitions.childhoodsSkillOffsets[childhood][i]
            bio.EP -= definitions.childhoodEPs[childhood]
            bio.age -= 15
            bio.path = opath
    if phase == 3:
        # pick way to distribute childhood ep to attributes
        opath = bio.path
        for attr in range(0, definitions.attributeCount):
            if bio.canIncreaseAttribute(attr):
                bio.path = bio.path + "|" + "+" + definitions.AttributeList[attr][0]
                bio.attributes[attr] += 1
                bio.EP -= bio.attributeIncreaseCost(attr)
                # print(bio.toCSV())
                explo(bio, phase, subphase + 1)
                # this needs to be enabled later
                # explo(bio,phase+1,0)
                bio.path = opath
                bio.attributes[attr] -= 1
                bio.EP += bio.attributeIncreaseCost(attr)
        explo(bio, phase + 1, 0)
    if phase == 4:
        print(bio.toCSV())


bio = biography.Biography()
explo(bio, 0, 0)
