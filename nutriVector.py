import nltk, re, string
import numpy as np
import sqlite3, ipdb
from nutrient import *
from foodItem import *

filterFile = "./nutrientsBase.txt"
conn = sqlite3.connect("sr28asc.db")
c = conn.cursor()
nutriFilter, nutris = GetNutrients(c, filterFile)

matrixFile = "foodNutrientMatrix.csv"
descFile = "foodNames.csv"
#f = open(matrixFile, "r")
if False: #f.closed():
  nutriDBIdFilter = [nutris[nutri][0] for nutri in nutriFilter]

  c.execute('SELECT * FROM FOOD_DES')
  dbFoods = c.fetchall()
  foods = []
  for i,item in enumerate(dbFoods):
    food = FoodItem(foodDesc=item)
    food.LoadNutrients(c, nutriDBIdFilter)
    foods.append(food)
    if i%100 == 0:
      print "."
    if i > 400: 
      break

  x = np.zeros((len(foods), len(nutriDBIdFilter)))
  descs = []
  for i,food in enumerate(foods):
    x[i,:] = food.x
    descs.append(food.GetDescription())
  np.savetxt("foodNutrientMatrix.csv", x);
  with open(descFile, "w") as f:
    for desc in descs:
      f.write(desc+"\n")
else:
  x = np.loadtxt(matrixFile)
  descs = []
  with open(descFile, "r") as f:
    for line in f.readlines():
      descs.append(line[:-1])
print "Done populating food nutrient matrix of shape {}".format(x.shape)
print "descriptions for {} foods".format(len(descs))

lens = np.sqrt((x**2).sum(axis=1))
import matplotlib.pyplot as plt
plt.plot(lens)
plt.show()

idSorted = np.argsort(lens)[::-1]
for i in idSorted[:10]:
  iMax = np.argmax(x[i,:])
  print lens[i], descs[i]
  print nutriFilter[iMax]

