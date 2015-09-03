__author__ = 'willkydd'

Attributes = [["End", "Endurance"],
              ["Str", "Strength"],
              ["Agi", "Agility"],
              ["Per", "Perception"],
              ["Int", "Intelligence"],
              ["Chr", "Charisma"]]

ChildHoodAttributeFloors = [35, 39, 0, 0, 0, 35]

Skills = [["wEdg", "Edge Weapons"],
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

Sexes = ["male", "female"]

sexAttributeOffsets = [[13, 16, 12, 13, 12, 12],
                       [15, 13, 12, 13, 12, 13]]

Childhoods = ["Nobility", "Wealthy Urban", "Town Trades", "Country Crafts", "Urban Commoners", "Country Commoners"]
childhoodAttributeOffsets = [[0, 0, 0, 0, 0, 0],
                             [-1, 0, 0, 1, 1, 0],
                             [-1, -1, 0, 1, 2, 0],
                             [0, 0, 1, 0, 1, 0],
                             [0, 1, 1, 0, -1, -1],
                             [1, 1, 1, 0, 0, -1]]
childhoodEPOffsets = [89, 90, 93, 94, 96, 97]
# somex=15
# childhoodEPOffsets = [somex, somex, somex, somex, somex, somex]
childhoodSkillOffsets = [[5, 4, 1, 4, 0, 4, 0, 2, 5, 2, 4, 2, 2, 0, 0, 1, 0, 3, 1],
                         [4, 3, 0, 3, 0, 0, 3, 2, 5, 1, 5, 1, 5, 1, 1, 1, 2, 2, 0],
                         [4, 5, 0, 3, 0, 0, 4, 1, 4, 1, 4, 0, 1, 1, 5, 1, 3, 0, 0],
                         [4, 3, 0, 4, 1, 4, 1, 0, 2, 1, 3, 0, 1, 1, 4, 1, 0, 0, 3],
                         [4, 4, 0, 3, 3, 0, 2, 0, 2, 1, 2, 0, 0, 1, 1, 4, 4, 0, 0],
                         [3, 3, 4, 3, 3, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 3, 0, 1, 4]]

Professions = ["Recruit", "Soldier", "Veteran", "Captain", "Hunter",
               "Bandit", "Peasant", "Village Schulz", "Noble Heir", "Courtier",
               "Knight", "Manorial Lord", "Hermit", "Novice Monk/Nun", "Friar",
               "Priest", "Abbot", "Bishop", "Oblate", "Student",
               "Clerk", "Physician", "Professor", "Alchemist", "Master Alchemist",
               "Vagabond", "Peddler", "Local Trader", "Travelling Merchant", "Merchant Proprietor",
               "Laborer", "Apprentice Craftsman", "Journeyman Craftsman", "Master Craftsman", "Thief",
               "Swindler"]

professionEPOffsets = [18, 18, 21, 17, 20, 22, 28, 24, 21, 12, 16, 16, 20, 23, 23, 12, 23, 23, 18, 22, 24, 27, 21, 24,
                       22, 20, 27, 23, 22, 17, 23]
professionAttributeOffsets = [[1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [1, 1, 0, 0, 0, -1], [-1, 0, 0, 0, 1, 1],
                              [1, -1, 1, 0, 1], [1, 0, 1, 0, 0, -1],
                              [1, 1, 0, 0, -1, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, -1, 1, 1], [0, -1, 0, 1, 1, 1],
                              [1, 1, 1, 0, 0, 0], [0, -1, 0, 0, 1, 2],
                              [1, 1, 0, 1, 0, -1], [0, 0, 0, 0, 1, 0], [0, 0, 0, -1, 1, 0], [1, 0, 0, -1, 0, 1],
                              [0, -1, 0, 1, 1, 1], [-1, -1, 0, 1, 1, 1], [0, -1, 0, 1, 1, 1],
                              [0, 0, 0, 0, 1, -1], [0, 0, 0, 1, 1, 0], [0, -1, 0, 1, 1, 0], [-1, -1, 0, 1, 1, 0],
                              [-1, -1, 0, 1, 2, 0], [0, -1, 0, 1, 1, 0], [-1, -1, 0, 1, 2, 0],
                              [1, 0, 1, 0, 0, -1], [0, 0, 0, 1, 1, 0], [0, -1, 0, 1, 1, 1], [0, 0, 0, 1, 1, 1],
                              [-1, -1, 0, 1, 1, 1],
                              [1, 1, 0, 0, -1, 0], [0, 0, 1, 0, 1, -1], [0, -1, 1, 1, 0, 0], [-1, 0, 0, 1, 1, 1],
                              [0, 0, 1, 0, 1, -1], [0, -1, 1, 1, 1, 1]]
professionSkillOffsets = []
professionBonusSkillOffsets = []
