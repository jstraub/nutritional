import nltk, re, string
import numpy as np
import sqlite3, ipdb
from nutrient import *
from foodItem import *

bowTerms = []
df = []
with open("./unique_terms.txt", "r") as f:
  bowTerms = f.readline().split(" ")
  df = np.array([float(dfw) for dfw in f.readline().split(" ")])
print "read {} unique BOW terms.".format(len(bowTerms))

filterFile = "./nutrientsBase.txt"
conn = sqlite3.connect("sr28asc.db")
c = conn.cursor()
nutrientFilter, nutris = GetNutrients(c, filterFile)

printDistMatrix = True
matchThrA = 88.
matchThrB = 89.

ranking = dict()
for nutrient in nutrientFilter:
  print nutrient
  n = nutris[nutrient]
  c.execute('SELECT * FROM NUT_DATA WHERE Nutr_No = "{}"'.format(n[0]))
  x = c.fetchall()
  printed = []
  nReject = 0
  for i,xi in enumerate(sorted(x, key=lambda x : float(x[2]))[::-1]):
    c.execute('SELECT * FROM FOOD_DES WHERE NDB_No = "{}"'.format(xi[0]))
    fitemA = FoodItem(c.fetchone())
    fitemA.AddNutrient(Nutrient(n, xi))
    valA = fitemA.GetNutrient(nutrient).GetValue();
    match = -1
    matchAngle = 90.
    for i,item in enumerate(printed):
      itemValue = float(item[0])
      matchAngle = fitemA.ComputeTFIDFangle(item[1], bowTerms, df)
      valB = item[1].GetNutrient(nutrient).GetValue();
      # reject based on a low match angle outright and if the
      # similarity is less clear also use the nutrient values to reject
      # food items with similar nutirent values.
      if matchAngle < matchThrA or \
          (matchThrA <= matchAngle and matchAngle < matchThrB and \
              np.abs((valA-valB)/valA) < 0.1):
        match = i
        break
    if match >= 0:
      nReject += 1
      continue
    # reject all descriptions that are artificial compositions of food
    # and all that are contain product/companie names (these are all
    # CAPS in the db)
    if not re.search("babyfood|cereal|newborn|infant formula|child formula|formulated bar|beverages|snacks|snack|gelatin desserts|gelatin dessert|leavening agents",
        fitemA.longDesc.lower()) and \
      not re.search("[A-Z][A-Z]+",fitemA.longDesc):
      print "\t{}\t{}\t{}".format(xi[2], n[1].encode("utf-8"),fitemA.longDesc)
      printed.append([xi[2],fitemA])
    if len(printed) >= 10: 
      break
  ranking[nutrient] = printed
  print "# duplicates rejected {}".format(nReject)
  if printDistMatrix:
    D = np.zeros((len(printed), len(printed)))
    for i,foodA in enumerate(printed):
      for j,foodB in enumerate(printed):
        D[i,j] = foodA[1].ComputeTFIDFangle(foodB[1], bowTerms, df)
    np.set_printoptions(precision=2, suppress=True)
    print D

print "<ul>"
for nutrient in nutrientFilter:
  print '<li>[expand title="{}"]'.format(nutrient)
  print '[table class="table-condensed" caption="{}" width="100%" colalign="center|center|left"]'.format(nutrient)
  print "rank, amount, food description"
  for rank,rankedFood in enumerate(ranking[nutrient]):
    value = rankedFood[0]
    food = rankedFood[1]
    unit = food.GetNutrient(nutrient).GetUnit()
    print "{}, {}{}, {}".format(rank+1,value, unit,
        re.sub(",",";",food.GetDescription())) 
  print "[/table][/expand]</li>"
print "</ul>"
conn.close()
