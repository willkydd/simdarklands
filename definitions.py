__author__ = 'willkydd'

AttributeList = [["End", "Endurance"],
                 ["Str", "Strength"],
                 ["Agi", "Agility"],
                 ["Per", "Perception"],
                 ["Int", "Intelligence"],
                 ["Chr", "Charisma"]]

SkillList = [["wEdg", "Edge Weapons"],
             ["wImp", "Imp Weapons"],
             ["wFll", "Foil"],
             ["wPol", "Polearms"],
             ["wThr", "Thrown Weapons"],
             ["wBow", "Bows"],
             ["wMsD", "Missile Weapons"],

             ["Alch", "Alchemy"],
             ["Relg", "Religion"],
             ["SpkC", "Common"],
             ["SpkL", "Latin"],
             ["R&W", "Reading & Writing"],

             ["Heal", "Healing"],
             ["Artf", "Artificing"],
             ["Stlh", "Stealth"],
             ["StrW", "Streetwise"],
             ["Ride", "Riding"],
             ["WdWs", "Woodwise"]]

sexList = ["undefined", "male", "female"]

sexAttributes = [[0, 0, 0, 0, 0, 0],
                 [13, 16, 12, 13, 12, 12],
                 [15, 13, 12, 13, 12, 13]]

childhoods = ["Nobility", "Wealthy Urban", "Town Trades", "Country Crafts", "Urban Commoners", "Country Commoners"]
childhoodsAttributeOffsets = [[0, 0, 0, 0, 0, 0],
                              [-1, 0, 0, 1, 1, 0],
                              [-1, -1, 0, 1, 2, 0],
                              [0, 0, 1, 0, 1, 0],
                              [0, 1, 1, 0, -1, -1],
                              [1, 1, 1, 0, 0, -1]]
childhoodEPs = [89, 90, 93, 94, 96, 97]
childhoodsSkillOffsets = [[5, 4, 1, 4, 0, 4, 0, 2, 5, 2, 4, 2, 2, 0, 0, 1, 0, 3, 1],
                          [4, 3, 0, 3, 0, 0, 3, 2, 5, 1, 5, 1, 5, 1, 1, 1, 2, 2, 0],
                          [4, 5, 0, 3, 0, 0, 4, 1, 4, 1, 4, 0, 1, 1, 5, 1, 3, 0, 0],
                          [4, 3, 0, 4, 1, 4, 1, 0, 2, 1, 3, 0, 1, 1, 4, 1, 0, 0, 3],
                          [4, 4, 0, 3, 3, 0, 2, 0, 2, 1, 2, 0, 0, 1, 1, 4, 4, 0, 0],
                          [3, 3, 4, 3, 3, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 3, 0, 1, 4]]

attributeCount = len(AttributeList)
skillCount = len(SkillList)
