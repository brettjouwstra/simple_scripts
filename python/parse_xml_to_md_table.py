import xml.etree.ElementTree as ET
tree = ET.parse("input_file.xml")
root = tree.getroot()
from pytablewriter import MarkdownTableWriter

class XmlDictConfig(dict):
    def __init__(self, parent_element):
        if parent_element.items():
            self.updateShim(dict(parent_element.items()))
        for element in parent_element:
            if len(element):
                aDict = XmlDictConfig(element)
                if element.items():
                    aDict.updateShim(dict(element.items()))
                self.updateShim({element.tag: aDict})
            elif element.items():
                self.updateShim({element.tag: dict(element.items())})
            else:
                try:
                    self.updateShim({element.tag: element.text.strip()})
                except:
                    self.updateShim({element.tag: element.text})

    def updateShim (self, aDict ):
        for key in aDict.keys():
            if key in self:
                value = self.pop(key)
                if type(value) is not list:
                    listOfDicts = []
                    listOfDicts.append(value)
                    listOfDicts.append(aDict[key])
                    self.update({key: listOfDicts})

                else:
                    value.append(aDict[key])
                    self.update({key: value})
            else:
                self.update(aDict)

def tableSetup():
    headers = []
    values = []
    for item in root:
        tmp = []
        a = XmlDictConfig(item)
        for k,v in a.items():
            if k not in headers:
                headers.append(k)
            tmp.append(str(v))
        values.append(tmp)
    return headers, values

def makeTable():
    writer = MarkdownTableWriter(
    table_name="Apps",
    headers=tableSetup()[0],
    value_matrix=tableSetup()[1],
    )
    writer.write_table()

print(makeTable())
