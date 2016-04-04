from sunlight import congress

def getBioGuideIds(legislators):
  ids = {}
  for legislator in legislators:
    crpId = legislator[0]
    leg = congress.legislators(crp_id=crpId, all_legislators=True)

    # if theres no leg, they didnt get elected
    if leg:
      bioguideId = leg[0]['bioguide_id']
      ids[bioguideId] = True

  return ids

def getVotes(billId):
  # Another bill here
  # hr4923-114
  results = congress.votes(roll_type='On Passage', bill_id=billId, fields='voters')
  return results[0]['voters']

