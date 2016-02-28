
def GetNutrients(c, filterFile=None):
  nutrientFilter = []
  with open(filterFile) as f:
    for line in f:
      if not line[0] == "#":
        nutrientFilter.append(line[:-1])

  c.execute('SELECT * FROM NUTR_DEF')
  nutris = dict()
  for n in c.fetchall():
    if n[3] in nutrientFilter:
      nutris[n[3]] = n
   
  return nutrientFilter, nutris

class Nutrient(object):
  def __init__(self, nutriDef, nutriData):
    self.nutriDef = nutriDef
    self.nutriData = nutriData
  def GetValue(self):
    return float(self.nutriData[2])
  def GetUnit(self):
    return self.nutriDef[1].encode("utf-8")
  def GetName(self):
    return self.nutriDef[3]
