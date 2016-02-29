import nltk, re, string, os.path, sys
import numpy as np
import sqlite3, ipdb
import matplotlib.pyplot as plt
from nutrient import *
from foodItem import *

filterFile = "./nutrientsBase.txt"
conn = sqlite3.connect("sr28asc.db")
c = conn.cursor()
nutriFilter, nutris = GetNutrients(c, filterFile)

matrixFile = "foodNutrientMatrix.csv"
descFile = "foodNames.csv"
#f = open(matrixFile, "r")
if not os.path.exists(matrixFile):
  nutriDBIdFilter = [nutris[nutri][0] for nutri in nutriFilter]

  c.execute('SELECT * FROM FOOD_DES')
  dbFoods = c.fetchall()
  foods = []
  for i,item in enumerate(dbFoods):
    food = FoodItem(foodDesc=item)
    food.LoadNutrients(c, nutriDBIdFilter)
    foods.append(food)
    if i%1000 == 0:
      print "{}".format(i)
    if i%100 == 0:
      sys.stdout.write(".")
      sys.stdout.flush()

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

# make all vector components sum up to 1 in one food item
xP = x.T + np.min(x, axis=1)
xP = xP/xP.sum(axis=0)
# compute entropy
H = -(xP*np.nan_to_num(np.log(xP))).sum(axis=0)

# whiten x
xW = x - np.mean(x, axis=0)
S = x.T.dot(x)
e,V = np.linalg.eigh(S)
e = np.sqrt(1./e)
xW = xW.dot(V.dot(np.diag(e)))

x = xW


lens = np.sqrt((x**2).sum(axis=1))
plt.plot(lens)
plt.plot(H)
plt.show()

idSorted = np.argsort(H)[::-1]
for i in idSorted[:100]:
  iMax = np.argmax(x[i,:])
  print H[i], descs[i]
#  print xP[:,i].T

idSorted = np.argsort(lens)[::-1]
for i in idSorted[:10]:
  iMax = np.argmax(x[i,:])
  print lens[i], descs[i]
  print nutriFilter[iMax]


