import itertools
import json

def init():
  data = openJSON('data/categories.json')['categories']['E0000']
  for L in range(0, len(data)+1):
    for subset in itertools.combinations(data, L):
      print(subset)

def openJSON(path):
  jsonData = open(path).read()

  data = json.loads(jsonData)
  return data

if __name__ == "__main__":
  init()
