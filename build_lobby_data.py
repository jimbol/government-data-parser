from sunlight import congress
import contributors
import numpy
import json
from collections import defaultdict

def init():
  # p = 'data/contributions.fec.2014.csv'
  # donors = contributors.init(p)
  # return donors

def createGraph():

  # reference model
  parent: {
    models: {
      type: Vote,
      ids: [1, 2, 3]
    }
  }

  # Get a list of models
  models = parent.get('models')

  # ==============================================

  # Schema
  legislators = {
    bioguid_id: {
      votes: [<vote ids>]

      # orgs who funded this leg
      organizations: [<organization ids>]
      industries: [<industry ids>]
    }
  }

  votes = {
    vote_id: {
      bill_id
      legislator_id

      # also may include info on specific votes
      # ie motion to add
    }
  }

  bills = {
    votes: [<vote ids>]
    issues: [<organization ids>]
  }


  issues = {
    lobbies: [<lobby ids>]

    # orgs who lobbied for this issue
    organizations: [<organization ids>]

    # industry for each org
    industries: [<industry ids>]
  }


  organizations = {
    industry_id

    lobbies: [<lobby ids>]

    # funded by this organization
    legislators: [<legislator ids>]
  }


  industries = {
    lobbies: [<lobby ids>]

    organizations: [<organization ids>]
    legislators: [<legislator ids>]
  }

  # with the goal being adding other properties to

def getRecipientTypes(donors):
  recipientTypes = numpy.array(donors['recipient_type'])
  recipients = numpy.array(donors['recipient_name'])
  allRecipientTypes = defaultdict(int)

  for i, leg in enumerate(recipients):
    recipientType = recipientTypes[i]

    allRecipientTypes[recipientType] += 1

  return allRecipientTypes
