import csv, io

def unicode2utf8(data):
  for line in data:
    yield line.encode('utf-8') 

def checkForTable(c, tableName):
  c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='{}'".format(tableName))
#  c.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_name='{}'".format(tableName))
  if c.fetchone():
    return True
  else:
    return False

fieldNames = {
    #Page 35 of documentation pdf
    "FOOD_DES.txt": ["NDB_No", "FdGrp_Cd", "Long_Desc", "Shrt_Desc",
      "ComName", "ManufacName", "Survey", "Ref_desc", "Refuse",
      "SciName", "N_Factor", "Pro_Factor", "Fat_Factor", "CHO_Factor"],
    "FD_GROUP.txt": ["FdGrp_Cd", "FdGrp_Desc"],
    "LANGUAL.txt": ["NDB_No", "Factor_Code"],
    "LANGDESC.txt": ["Factor_Code", "Description"],
    "NUT_DATA.txt": ["NDB_No", "Nutr_No", "Nutr_Val", "Num_Data_Pts",
      "Std_Error", "Src_Cd", "Deriv_Cd", "Ref_NDB_No", "Add_Nutr_Mark",
      "Num_Studies", "Min", "Max", "DF", "Low_EB", "Up_EB", "Stat_cmt",
      "AddMod_Date", "CC"],
    "NUTR_DEF.txt": ["Nutr_No", "Units", "Tagname", "NutrDesc",
      "Num_Dec", "SR_Order"],
    "SRC_CD.txt": ["Src_Cd", "SrcCd_Desc"],
    "DERIV_CD.txt": ["Deriv_Cd", "Deriv_Desc"],
    "WEIGHT.txt": ["NDB_No", "Seq", "Amount", "Msre_Desc", "Gm_Wgt",
      "Num_Data_Pts", "Std_Dev"],
    "FOOTNOTE.txt": ["NDB_No", "Footnt_No", "Footnt_Typ", "Nutr_No",
      "Footnt_Txt"],
    "DATSRCLN": ["NDB_No", "Nutr_No"],
    "DATA_SRC": ["DataSrc_ID", "Authors", "Title", "Year", "Journal",
      "Vol_City", "Issue_State", "Start_Page", "End_Page"]
    }

filename = "LANGUAL.txt"
filename = "LANGDESC.txt"
filename = "NUT_DATA.txt"
filename = "NUTR_DEF.txt"
filename = "SRC_CD.txt" 
filename = "DERIV_CD.txt"
filename = "WEIGHT.txt" #weight per unit for each food item
filename = "FOOTNOTE.txt"
filename = "FOOD_DES.txt"
filename = "FD_GROUP.txt"
path = "../sr28asc/"
if False:
  with io.open(path+filename, 'r', encoding="ISO-8859-1") as f:
    reader = csv.DictReader(f, fieldnames=fieldNames[filename],
        delimiter="^", quotechar="~")
    for row in reader:
      print row
else:
  import sqlite3, re
  conn = sqlite3.connect("sr28asc.db")
  conn.text_factory = str
  c = conn.cursor()
  for filename in ["LANGUAL.txt", "LANGDESC.txt", "NUT_DATA.txt",
      "NUTR_DEF.txt", "SRC_CD.txt", "DERIV_CD.txt", "WEIGHT.txt",
      "FOOTNOTE.txt", "FOOD_DES.txt", "FD_GROUP.txt"]:
    tableName = re.sub(".txt","",filename)
    fields = fieldNames[filename]
    if not checkForTable(c, tableName):
      print "table does not exist yet"
      cmd = 'CREATE TABLE {} ('.format(tableName) + ",".join(fields) + ")"
      print cmd
      c.execute(cmd)
      conn.commit()
    with io.open(path+filename, 'r', encoding="ISO-8859-1") as f:
      reader = csv.DictReader(unicode2utf8(f), fieldnames=fieldNames[filename],
          delimiter="^", quotechar="~")
      for row in reader:
        values = [] 
        for fieldname in fieldNames[filename]:
          values.append(row[fieldname])
        cmd = 'INSERT INTO {} VALUES ('.format(tableName.lower()) + ",".join(['?']*len(fields)) + ")"
        c.execute(cmd, tuple(values))
      conn.commit()
  conn.close()

