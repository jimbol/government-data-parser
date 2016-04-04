from sunlight import congress
from collections import defaultdict
import os
import json
import uuid

# legislator -------- ORGANIZATIONS
#     |                     |
#    vote ------ bill --- ISSUES


# SAMPLE LOOK-UPS
# Get all bills funded by inds



class Cycle:

  lastVoteId = 0

  votes = {}
  legislators = {}
  bills = {}

  def init(self):
    self.legislators = self.buildLegislatorHash()
    self.buildBillHash('hr', 113)
    self.buildBillHash('s', 113)

# build store

  def buildLegislatorHash(self):
    output = {}
    legs = congress.all_legislators_in_office()

    for leg in legs:
      keys = ['bioguide_id', 'crp_id', 'last_name', 'first_name', 'middle_name', 'gender', 'state', 'party', 'chamber']

      id = leg['bioguide_id']
      output[id] = self.pick(keys, leg)

      output[id]['votes'] = []

    return output

  def buildBillHash(self, path, congressNo):
    output = {}
    votes = {}
    path = 'data/bills/'+path+'/'
    # Dont worry about hres right now, its process stuff "house resolution"
    # Just use `hr` and `s`

    # Grab all folders in `hr`
    voteIds = os.listdir(path)

    # Loop through all these folders
    for id in voteIds:
      bill = self.openJSON(path + id + '/data.json')
      billId = id + '-' + str(congressNo)

      actions = bill['actions']

      for action in actions:
        if action['type'] == 'vote':

          bill['votes'] = []

          self.bills[billId] = bill

          self.createVotes(billId)

          break

    return output

  def createVotes(self, billId):
    rawVotes = congress.votes(bill_id=billId,
      roll_type='On Passage',
      fields='voter_ids')

    if rawVotes is None:
      return

    ids = rawVotes[0]['voter_ids']

    for key, value in ids.iteritems():
      self.lastVoteId += 1
      legislator = None

      # Create vote obj for each individual
      vote = {
        'vote': value,
        'bill': self.bills[billId]
      }

      # if we have a legislator for that id
      if self.legislators.get(key) != None:
        legislator = self.legislators[key]

        # Add it to the vote
        vote['legislator'] = legislator

        # Add vote to the legislator
        legislator['votes'].append(vote)

      self.bills[billId]['votes'].append(vote)
      self.votes[self.lastVoteId] = vote

# helpers

  def pick(self, keys, obj):
    output = {}

    for key in keys:
      output[key] = obj[key]

    return output

  def openJSON(self, path):
    jsonData = open(path).read()

    data = json.loads(jsonData)
    return data

c = Cycle()
# c.init()
# cycle.createVotes('hr10-113')

