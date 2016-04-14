from __future__ import division
import matplotlib.pyplot as plt
import numpy

def billsWithVotes(bills):
  print '@billsWithVotes - find all bills with votes'
  # TODO: Needs to be tested
  billsWithVotes = []

  for id, bill in bills.iteritems():
    if len(bill['votes']) > 0:
      billsWithVotes.append(bill)

  print 'Voted: ' + str(len(billsWithVotes))
  print 'Total: ' + str(len(bills))
  print ' Perc: ' + str(len(billsWithVotes)/len(bills))

  # return billsWithVotes

def billVotePercentage(bills):

  hRatios = []
  sRatios = []
  t = 0

  for id, bill in bills.iteritems():
    votes = bill.get('votes')

    if votes == None or len(votes) == 0:
      continue

    hr = {
      'Yea': 0,
      'Nay': 0,
      'Not Voting': 0,
      'Present': 0
    }

    s = {
      'Yea': 0,
      'Nay': 0,
      'Not Voting': 0,
      'Present': 0
    }



    for vote in votes:

      # This doesnt work since senate votes on HRs
      # and visa versa.  Must mark house while building
      # votes



      if vote.get('chamber') == 'house':
        hr[vote['vote']] += 1
      elif vote.get('chamber') == 'senate':
        s[vote['vote']] += 1
      else:
        continue

    hTotal = sum(hr.values())
    sTotal = sum(s.values())

    t+=1

    if hTotal > 0:
      hRatios.append(hr['Yea'] / hTotal)

    if sTotal > 0:
      sRatios.append(s['Yea'] / sTotal)

  print 'House: '
  print hRatios

  print 'Senate: '
  print sRatios
  print 'Total:'
  print t

  histogram=plt.figure()

  bins = numpy.linspace(0, 1, 25)

  plt.xlabel("Percent Yeas")
  plt.ylabel("Frequency")

  plt.title("House Votes")
  plt.hist(hRatios, bins, alpha=0.5)

  # plt.title("Senate Votes")
  # plt.hist(sRatios, bins, alpha=0.5)

  plt.show()





def billsResults(bills):
  h = {
    'p': [],
    'f': []
  }
  s = {
    'p': [],
    'f': []
  }

  passed = []
  failed = []

  for id in bills:
    bill = bills[id]
    sVote = bill['history'].get('senate_passage_result')
    hVote = bill['history'].get('house_passage_result')

    if sVote == 'pass' or hVote == 'pass':
      passed.append(bill)

    if sVote == 'fail' or hVote == 'fail':
      failed.append(bill)


    if sVote == 'pass':
      s['p'].append(bill)

    if sVote == 'fail':
      s['f'].append(bill)

    if hVote == 'pass':
      h['p'].append(bill)

    if hVote == 'fail':
      h['f'].append(bill)

  print 'H Passed: ' + str(len(h['p']))
  print 'H Failed: ' + str(len(h['f']))

  print 'S Passed: ' + str(len(s['p']))
  print 'S Failed: ' + str(len(s['f']))

  print 'Passed: ' + str(len(passed))
  print 'Failed: ' + str(len(failed))
  print 'Total: ' + str(len(bills))

  # return {
  #   'passed':passed,
  #   'failed': failed
  # }

def committeeBreakdown(committees):
  coms = []
  withVote = []
  withoutVote = []
  withVoteRatios = []
  withoutVoteRatios = []

  labels = []

  for committeeId in committees:

    billCount = len(committees[committeeId]['bills'])

    coms.append((committeeId,
      billCount
    ))

    # average num of bills not voted on/voted on
    voted = 0
    notVoted = 0

    for bill in committees[committeeId]['bills']:
      if bill.get('votes') != None:
        voted+=1
      else:
        notVoted+=1

    labels.append(committeeId)
    withVote.append(voted)
    withoutVote.append(notVoted)
    total = notVoted + voted

    if total > 0:
      withVoteRatios.append(voted / total)
      withoutVoteRatios.append(notVoted / total)

  # print sorted(coms, key=getKey)


  # plt.title("% of bills that made it to vote by committee")

  # plt.xlabel("bills voted on / total")
  # plt.ylabel("frequency")

  # plt.hist(withVoteRatios)
  # plt.show()



  plt.title("Bills by committee")

  plt.xlabel("bills voted on / total")
  plt.ylabel("frequency")

  width = 0.8
  ind = numpy.arange(len(labels))

  p1 = plt.bar(ind, withVote, width, color='r')
  p2 = plt.bar(ind, withoutVote, width, color='y', bottom=withVote)


  plt.legend(('Voted', 'Not voted'))

  plt.show()

  # Mean
  print 'Voted:'
  print sum(withVote) / float(len(withVote))
  print 'Not voted:'
  print sum(withoutVote) / float(len(withoutVote))
  print 'Mean:'
  print sum(com[1] for com in coms) / float(len(coms))

def run(c):
  # billsWithVotes(c.bills)
  billsResults(c.bills)
  print '=============================='
  committeeBreakdown(c.committees)



def getKey(item):

  return item[1]
