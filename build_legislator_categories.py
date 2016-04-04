from sunlight import congress
import contributors
import numpy
import json
from collections import defaultdict

def init():
  # p = 'csv/sample.csv'
  p = 'csv/contributions.fec.2014.csv'
  donors = contributors.init(p)
  getFundedLegislators(donors)

def getFundedLegislators(donors):
  ids = numpy.array(donors['recipient_ext_id'])
  recipientTypes = numpy.array(donors['recipient_type'])
  amounts = numpy.array(donors['amount'])
  contributorCategories = numpy.array(donors['contributor_category'])
  recipients = numpy.array(donors['recipient_name'])

  # outputs categories by legistlators
  # and legislators by category
  fundedLegs = defaultdict(lambda: defaultdict(int))
  categoryLegs = defaultdict(lambda: defaultdict(int))

  for i, leg in enumerate(recipients):
    recipientType = recipientTypes[i]

    # Only look at Politicians
    if recipientType != "P":
      continue

    # For each legislator
    # get bioguide_id
    bioguideId = getBioguideID(ids[i])

    # No bioguide, not elected. Only look at elected legislators
    if not bioguideId:
      continue

    # the contributor's category
    contributorCategory = contributorCategories[i]

    # update category funded legislators
    categoryLegs[contributorCategory][bioguideId] += amounts[i]

    # update funded legislators hash by category
    fundedLegs[bioguideId][contributorCategory] += amounts[i]

  save('tmp/legislator_category_amounts.json', fundedLegs)
  save('tmp/category_legislator_amounts.json', categoryLegs)

idHash = defaultdict(str)
unelected = defaultdict(str)

def getBioguideID(crpId):
  if unelected[crpId]:
    return

  bioguideId = idHash[crpId]

  if bioguideId:
    print 'Use lookup,', crpId
    return bioguideId

  print 'Fetching', crpId
  leg = congress.legislators(crp_id=crpId, all_legislators=True)

  # if theres no leg, they didnt get elected
  if leg:
    bioguideId = leg[0]['bioguide_id']
    idHash[crpId] = bioguideId
    return bioguideId
  else:
    unelected[crpId] = True

def save(path, data):
  with open(path, 'w') as f:
    print '- Writing file:', path
    f.write(json.dumps(data))
    f.close()

if __name__ == "__main__":
  init()
