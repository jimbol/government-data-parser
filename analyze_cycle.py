from __future__ import division

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

  # return {
  #   'passed':passed,
  #   'failed': failed
  # }
