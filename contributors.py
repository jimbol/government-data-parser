'''
#getProperties
Creates hash of csv results by colum

#getTopOrganizations(ORGANIZATIONS, AMOUNTS)
Returns nparray of top contributing organizations

#getFundedLegislators(ORG_NAME, LEGISLATOR_COLUM, ORG_COLUM, AMOUNT_COLUM, TYPE_COLUM, PARTY_COLUM)
Returns legislators funded by

'''

import csv
import sys
import time
import numpy
from collections import defaultdict
import datetime
import matplotlib.pyplot as plt
import operator

def init(fileName):
  if not fileName:
    fileName = sys.argv[1]
  f = open(fileName, 'rt')

  return getProperties(f)

def getProperties(f):
  formattedData = defaultdict(list)
  donors = csv.reader(f)
  keys = next(donors)

  try:
    # for each row (donor)
    # loop through the keys
    # and add each value to
    # corresponding formattedData key
    for donor in donors:

      for i, key in enumerate(keys):
        value = donor[i]

        # we can add other type handlers here

        if key == 'amount':
          value = float(value)
          amount = value or 0

        if key == 'date':
          value = parseDate(value)

        formattedData[key].append(value)

  finally:
    f.close()

  return formattedData

def getFundedLegislators(source, donors):
  ids = numpy.array(donors['recipient_ext_id'])
  types = numpy.array(donors['recipient_type'])
  amounts = numpy.array(donors['amount'])
  categories = numpy.array(donors['contributor_category'])
  legislators = numpy.array(donors['recipient_name'])
  organizations = numpy.array(donors['organization_name'])

  fundedLegs = defaultdict(int)

  for i, leg in enumerate(legislators):
    leg = cleanLegislatorName(leg)
    legOrg = organizations[i]
    legCat = categories[i]
    legType = types[i]
    legID = ids[i]

    if legType == "P" and isLegislatorFunded(source, legOrg, legCat):
      amount = amounts[i]

      fundedLegs[legID] += amount

  return sortHash(fundedLegs)

# TODO
# This does look up by organization OR category
# Choose one
def isLegislatorFunded(source, legOrg, legCat):
  if type(source) is list:
    if legCat in source:
      return True

  if type(source) is str:
    if source == legOrg:
      return True

  return False

# PARSERS
# move parsers into another file

def parseDate(dateString):
  if not dateString:
    return datetime.datetime.today()

  d = dateString.split('-')
  return datetime.date( int(d[0]), int(d[1]), int(d[2]) )

def cleanLegislatorName(leg):
  return leg[:-4]







# Not currently used
def getTopOrganizations(orgs, amounts):
  organizations = defaultdict(int)

  for i, org in enumerate(orgs):
    amount = amounts[i]
    organizations[org] += amount

  return sortHash(organizations)

def sortHash(obj):
  sorted_hash = sorted(obj.items(), key=operator.itemgetter(1))
  return sorted_hash


if __name__ == "__main__":
  init(sys.argv[1])
