__author__ = 'willkydd'
import definitions


class Biography:
    attributes = [0] * definitions.attributeCount
    skills = [0] * definitions.skillCount
    sex = 0

    def oneLine(self):
        return definitions.sexList[self.sex][1] + " | " + \
               str(self.attributes) + " | " + str(self.skills)

    def toCSV(self):
        return definitions.sexList[self.sex][1] + ", " + \
               str(self.attributes).strip("[]") + ", " + str(self.skills).strip("[]")

    def setSex(self, tsex):
        self.attributes = definitions.sexAttributes[tsex]
        self.sex = tsex
