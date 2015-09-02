__author__ = 'willkydd'

AttributeList = [[0, "End", "Endurance"],
                 [2, "Str", "Strength"],
                 [3, "Agi", "Agility"],
                 [4, "Per", "Perception"],
                 [5, "Int", "Intelligence"],
                 [6, "Chr", "Charisma"]]

SkillList = [[0, "wEdg", "Edge Weapons"],
             [1, "wImp", "Imp Weapons"],
             [2, "wFll", "Foil"],
             [3, "wPol", "Polearms"],
             [4, "wThr", "Thrown Weapons"],
             [5, "wBow", "Bows"],
             [6, "wMsD", "Missile Weapons"],

             [7, "Alch", "Alchemy"],
             [8, "Relg", "Religion"],
             [9, "SpkC", "Common"],
             [10, "SpkL", "Latin"],
             [11, "R&W", "Reading & Writing"],

             [12, "Heal", "Healing"],
             [13, "Artf", "Artificing"],
             [14, "Stlh", "Stealth"],
             [15, "StrW", "Streetwise"],
             [16, "Ride", "Riding"],
             [17, "WdWs", "Woodwise"]]

sexList = [[0, "undefined"],
           [1, "male"],
           [2, "female"]]

sexAttributes = [[0, 0, 0, 0, 0, 0],
                 [13, 16, 12, 13, 12, 12],
                 [15, 13, 12, 13, 12, 13]]

attributeCount = len(AttributeList)
skillCount = len(SkillList)
