'''
Vote: H.R. 8
  bill_id: hr8-114
  roll_type: On%20Passage
Industy: Oil
  contributor_category: E1100, E1110, E1120, E1140, E1150, E1160, E1170, E1180

Sunlight Url
Votes: http://congress.api.sunlightfoundation.com/votes?roll_type=On%20Passage&bill_id=hr8-114&apikey=66603c029b1b49428da28d6a783f795e&fields=voters
Category Codes: https://github.com/sunlightlabs/brisket/blob/master/data/docs/catcodes.csv

NEXT STEPS:
Should be able to take many combiniations of categories at once.
  [
    "1",
    "2",
    "3",
    [
      "1",
      "2"
    ],
    [
      "1",
      "3"
    ],
    [
      "2",
      "3"
    ]
  ]

Which gives breakdowns like:
  '1': {<results>}
  '2': {<results>}
  '3': {<results>}
  '1 2': {<results>}
  '1 3': {<results>}
  '2 3': {<results>}

'''

import contributors
import congress
import math
import numpy
import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy import stats
import json
import datetime

# Public
def init(splitResults):
  # oil/gas categories
  categories = ["E1100", "E1110", "E1120", "E1140", "E1150", "E1160", "E1170", "E1180"]

  # p = 'csv/sample.csv
  p = 'csv/contributions.fec.2014.csv'

  fundedIds = loadIdsFromCSV(p, categories, splitResults)

def run(combineResults=True):
  billId = 'hr8-114'
  categories = ["E1100", "E1110", "E1120", "E1140", "E1150", "E1160", "E1170", "E1180"]
  breakdowns = defaultdict(dict)

  if combineResults:
    breakdowns['all'] = testCategory(billId, 'all')
  else:
    for categoryId in categories:
      breakdowns[categoryId] = testCategory(billId, categoryId)

  save('tmp/category_breakdowns', breakdowns)

# Private
def testCategory(billId, categoryId):
  fundedIds = loadIdsFromJSON()
  votes = congress.getVotes(billId)

  catLegIds = fundedIds[categoryId]

  breakdown = getVoteBreakdown(catLegIds, votes)

  print 'Testing category ', categoryId
  twoProportionHypothesisTest(breakdown)
  plot(breakdown, categoryId)

  return breakdown

def loadIdsFromCSV(p, categories, combineResults=True):
  donors = contributors.init(p)

  fundedIds = defaultdict(dict)

  if combineResults:
    catLegislators = contributors.getFundedLegislators(categories, donors)
    catLegIds = congress.getBioGuideIds(catLegislators)
    fundedIds['all'] = catLegIds

  else:

    for categoryId in categories:
      print 'fetching legislators for', categoryId
      print datetime.datetime.now().time().isoformat()

      catLegislators = contributors.getFundedLegislators([categoryId], donors)
      catLegIds = congress.getBioGuideIds(catLegislators)

      print datetime.datetime.now().time().isoformat()

    fundedIds[categoryId] = catLegIds

  save('tmp/category_legislator_ids.json', fundedIds)

  return fundedIds

def loadIdsFromJSON():
  path = 'tmp/category_legislator_ids.json'
  with open(path) as jsonFile:
    fundedIds = json.loads(jsonFile.read())

  return fundedIds


def plot(r, name):

  N = 2
  yes = (r['funded']['Yea'], r['unfunded']['Yea'])
  no =  (r['funded']['Nay'], r['unfunded']['Nay'])

  ind = numpy.arange(N)
  width = 1

  p1 = plt.bar(ind, yes, width, color='r')
  p2 = plt.bar(ind, no, width, color='y', bottom=yes)

  plt.ylabel('Votes')
  plt.title('Votes by funding status for category: '+name)
  # plt.title('Votes by funding status')
  plt.xticks(ind + width/2., ('funded', 'unfunded'))
  plt.yticks(numpy.arange(0, 365, 50))
  plt.legend((p1[0], p2[0]), ('Yea', 'Nay'))

  name = 'tmp/' + name + '.png'
  plt.savefig(name, bbox_inches='tight')
  plt.close()
  # plt.show()

def save(path, data):
  with open(path, 'w') as f:
    print 'writing file'
    f.write(json.dumps(data))
    f.close()

def getVoteBreakdown(fundedIds, votes):
  total = 0
  funded = defaultdict(float)
  unfunded = defaultdict(float)

  for bioguideId, voteHash in votes.iteritems():
    vote = voteHash['vote']
    total = total + 1

    if fundedIds.get(bioguideId, False):
      funded[vote] = funded[vote] + 1
      funded['total'] = funded['total'] + 1
    else:
      unfunded[vote] = unfunded[vote] + 1
      unfunded['total'] = unfunded['total'] + 1

  return {
    'funded': funded,
    'unfunded': unfunded,
    'total': total
  }

def twoProportionHypothesisTest(breakdown):
  fYea = breakdown['funded']['Yea']
  fNay = breakdown['funded']['Nay']
  fTotal = fYea + fNay

  fProportion = fYea / fTotal

  uYea = breakdown['unfunded']['Yea']
  uNay = breakdown['unfunded']['Nay']
  uTotal = uYea + uNay

  uProportion = uYea / uTotal


  # START HERE
  # Why is pHat never changing?

  print fYea + uYea
  print fTotal + uTotal
  pHat = (fYea + uYea) / (fTotal + uTotal)
  print 'pHat: ', pHat

  term = pHat * (1 - pHat)

  Z = (fProportion - uProportion) / math.sqrt((term / fTotal) + (term / uTotal))
  print 'Z: ', Z

  pValue = (1 - getPValue(Z)) * 2
  print 'P-value: ', pValue

def getPValue(Z):
  return stats.norm(0, 1).cdf(Z)

# init(True)
run()
