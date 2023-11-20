import numpy as np
from numpy import random
import json

from human import Human
from land import Land
from deal import Commerce, Usury

import copy


ppl = []
rng = np.random.default_rng()


def run():
  # Creates the people
  global ppl

  MAX_PROFIT = 10
  MAX_START = 100.0
  N = 1000
  N_LANDS = 5
  LOAN_AMOUNT = MAX_PROFIT

  for i in range(100):
    money = rng.random() * MAX_START
    env_con = 0.5
    ppl.append(Human(i, money, env_con))

  moneys = np.array([x.money for x in ppl])

  results = {}
  results['mean'] = np.mean(moneys)
  results['STD'] = np.std(moneys)
  results['result'] = []

  counter = 0

  for type in ['commerce','usury']:   
    for LOAN_AMOUNT in [MAX_PROFIT/4.0, MAX_PROFIT/3.0, MAX_PROFIT/2.0, MAX_PROFIT]:
        for INTEREST_RATE in [0.02, 0.03, 0.05, 0.13, 0.25, 0.31, 0.55]:
          for i in range(50):
            print(str(round(counter/float(2*4*7*50) *100, 2)), '% klaar,')
            
            lands = []
            for i in range(N_LANDS):
              lands.append(Land(i, MAX_PROFIT))
            
            result = {}
            result['type'] = type
            result['LOAN_AMOUNT'] = LOAN_AMOUNT

            res = None
            if type == 'usury':
              result['interest'] = INTEREST_RATE
              res = deal(type, ppl, lands, LOAN_AMOUNT, N, INTEREST_RATE)
            else:
              res = deal(type, ppl, lands, LOAN_AMOUNT, N, 0.0)

            result['mean'] = res['mean']
            result['STD'] = res['STD']
            result['percentiles'] = res['percentiles']

            result['need'] = res['need']
            result['greed'] = res['greed']

            result['deals_done'] = len(res['deals'])
            result['deals_annuled'] = res['deals_annuled']
            result['lands_health'] = res['lands_health']
            # result['ppl'] = res['ppl']
            

            results['result'].append(result)
            counter += 1
      
  results['MAX_PROFIT'] = MAX_PROFIT
  results['N'] = N_LANDS*N
  

  with open('results.json', mode='w', encoding='utf-8') as file:
    json.dump(results, file)


      

def deal(type, ppl, lands, amount, n, r):
  global rng
  deals = []
  ppls = copy.deepcopy(ppl)
  landz = copy.deepcopy(lands)
  deals_annuled = 0
  result = {}

  for t in range(n):
    # This sections chooses a random loaner and a random worker
    # Only condition is that the loanee can not have negative funds
    sorted_ppl = sorted(ppls, key=lambda x: x.money)

    try:
      loan_possible_index = np.where(np.array([p.money for p in sorted_ppl]) > amount)[0][0]
    except:
      continue

    for land in landz:
      loaner_i = rng.integers(loan_possible_index, len(ppl))
      worker_i = rng.integers(loaner_i+1)

      worker = sorted_ppl[worker_i]
      loaner = sorted_ppl[loaner_i]

      # Skip to the next one if loaner doesn't have enough money to lend
      deal = None
      if (type == "commerce"):
        deal = Commerce(t, loaner, worker, land, amount)
      if (type == "usury"):
        deal = Usury(t, loaner, worker, land, amount, r)
      
      if not deal.is_possible():
        continue
      deal.execute(ppls)

      if deal.annuled:
        #This is the case when the deal was annuled due to environmental reasons
        deals_annuled += 1
        land.health += (1 - land.health) / 4.0
      else:
        loaner_info = loaner.get_need_greed(ppls)
        loaner_info = (loaner_info[0], loaner_info[1], loaner.env_con)
        loaner_info = [round(x, 2) for x in loaner_info] + [loaner.money]
        
        worker_info = worker.get_need_greed(ppls)
        worker_info = (worker_info[0], worker_info[1], worker.env_con)
        worker_info = [round(x, 2) for x in worker_info] + [worker.money]

        if not deal.annuled:
          deals.append({
              'loaner': loaner_info,
              'worker': worker_info,
              'amount': amount, 
              'loss': deal.loss,
          })

  result['ppl'] = ppls

  moneys = np.array([x.money for x in ppls])
  result['mean'] = np.mean(moneys)
  result['STD'] = np.std(moneys)

  result['deals'] = deals

  # result['need'] = np.mean(np.array([(x['loaner'][0]+x['worker'][0])/2 for x in deals]))
  result['need'] = np.mean(np.array([person.get_need_greed(ppls)[0] for person in ppls]))
  result['greed'] = np.mean(np.array([person.get_need_greed(ppls)[1] for person in ppls]))
  # result['greed'] = np.mean(np.array([(x['loaner'][1]+x['worker'][1])/2 for x in deals]))
  # result['env_con'] = np.mean(np.array([(x['loaner'][2]+x['worker'][2])/2 for x in deals]))
  result['percentiles'] = [np.percentile(moneys, q) for q in range(1,100,24)]

  result['deals_annuled'] = float(deals_annuled)
  result['lands_health'] = np.mean(np.array([l.health for l in landz]))
  result['ppl'] = [person.serialize(ppls) for person in ppls]



  return result


run()