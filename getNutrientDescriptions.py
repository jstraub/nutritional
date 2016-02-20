import urllib, json

url = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles=Folic_acid"

response = urllib.urlopen(url)
if not response:
  print "no response"
  exit(1)

data = json.loads(response.read())
print data
print json.dumps(data, sort_keys=True, indent=2)
print data["query"]["pages"]["21721040"]["extract"]

