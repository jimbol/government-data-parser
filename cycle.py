from sunlight import congress
from collections import defaultdict
import os
import json
import csv
import uuid


# legislator -------- organizations
#   |  |  |                 |
#   |  |  sponsor -         |
#   |  |           |        |
#   |  |           |        |
#   |  -- vote -- bill --- issues
#   |              |
#   |              |
# committee - committee activity


# Legislator baselines
# - Average vote (Y/N)
# - The average vote for Passage votes will mostly be Yea

# COMMITTEE { name, legislators, bills, other-goodies }

class Cycle:

  lastVoteId = 0
  lastCommitteeActivityId = 0

  votes = {}
  legislators = {}
  bills = {}
  committees = {}
  committeeActivities = {}

  def init(self):
    # self.legislators = self.buildLegislators()
    # self.buildBills('hr', 113)
    # self.buildBills('s', 113)
    self.buildLobbying()

# build stores

  def buildLegislators(self):
    output = {}
    legs = congress.all_legislators_in_office()

    for leg in legs:
      keys = ['bioguide_id', 'crp_id', 'last_name', 'first_name', 'middle_name', 'gender', 'state', 'party', 'chamber']

      id = leg['bioguide_id']
      output[id] = self.pick(keys, leg)

      output[id]['votes'] = []

    return output

  def buildLobbying(self):
    with open('data/lobbying/lob_lobbying.txt', 'rb') as csvfile:
      lobbyReader = csv.reader(csvfile, quotechar='|')
      output = defaultdict(int)
      for row in lobbyReader:
        id = row[0]
        registrant_raw = row[1]
        registrant = row[2]
        is_firm = row[3]
        client_raw = row[4]
        client = row[5]
        ult_org = row[6]
        amount = row[7]
        catcode = row[8]
        source = row[9]
        self_filer = row[10]
        include_nsfs = row[11]

        if len(amount):
          output[registrant] += float(amount)

        # print l['self_filer']

        # print isFirm

        # print row[4]

      o = []
      for key in output:
        o.append((key, output[key]))

      a = sorted(o, key=lambda x: x[1])
      print a[0]
      print a[1]
      print a[2]
      print a[3]
      print a[4]
      # print sorted(output)
      # print len(output)

  def buildBills(self, path, congressNo):

    # TODO, clean up this function DAMNIT!

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

      # save bill in store
      self.bills[billId] = bill
      actions = bill['actions']


      # move committees
      committees = bill['committees']
      bill['rawCommittees'] = committees
      bill['committees'] = []

      bill['committeeActivities'] = []

      self.setUpCommittees(committees, bill)

      # Create vote for each vote acion
      for action in actions:
        if action['type'] == 'vote':
          if bill.get('votes') == None:
            bill['votes'] = []

          self.buildVotesForBill(billId)

    return output

  def setUpCommittees(self, committees, bill):
    # Build committee obj and committee actions
    # Add both to the bill
    for committee in committees:
      id = committee['committee_id']
      outputCommittee = self.committees.get(id)

      # create obj to stor committee if none exists
      if outputCommittee == None:
        outputCommittee = {
          'name': committee['committee'],
          'committeeActivities': [],
          'bills': []
        }

        self.committees[id] = outputCommittee

      for activity in committee['activity']:
        committeeActivity = {
          'activity': activity,
          'bill': bill,
          'committee': outputCommittee
        }

        # save activity on class
        self.lastCommitteeActivityId += 1
        self.committeeActivities[self.lastCommitteeActivityId] = committeeActivity

        # and on committee
        outputCommittee['committeeActivities'].append(committeeActivity)

      outputCommittee['bills'].append(bill)
      bill['committees'].append(outputCommittee)

  def buildVotesForBill(self, billId):
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
        vote['chamber'] = legislator['chamber']

        legislator.keys()

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
c.init()
# cycle.createVotes('hr10-113')

