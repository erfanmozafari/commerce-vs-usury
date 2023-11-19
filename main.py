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
  INTEREST_RATE = 0.3
  LOAN_AMOUNT_COM = MAX_PROFIT
  LOAN_AMOUNT_USU = LOAN_AMOUNT_COM

  for i in range(100):
    money = rng.random() * MAX_START
    env_con = 0.5
    ppl.append(Human(i, money, env_con))

  moneys = np.array([x.money for x in ppl])

  results = {}
  results['mean'] = np.mean(moneys)
  results['STD'] = np.std(moneys)
  results['result'] = []

  for i in range(5):
    for type in ['commerce', 'usury']:    
        lands = []
        for i in range(N_LANDS):
          lands.append(Land(i, MAX_PROFIT))
        
        result = {}
        result['MAX_PROFIT'] = MAX_PROFIT
        # result['N_LANDS'] = N_LANDS
        # result['N'] = N

        res = None
        if type == 'usury':
          result['interest'] = INTEREST_RATE
          res = deal(type, ppl, lands, LOAN_AMOUNT_USU, N, INTEREST_RATE)
        else:
          result['amount'] = LOAN_AMOUNT_COM
          res = deal(type, ppl, lands, LOAN_AMOUNT_COM, N, 0.0)

        # result['init_ppl'] = [p.serialize(ppl) for p in ppl]

        # moneys1 = [p.money for p in ppl]
        # print("MEAN: " + str(np.mean(moneys1)) + '\n' + "STD: " + str(np.std(moneys1)))

        # commerce()
        # print(str(deals_annuled) + ' deals annuled.')
        # print([round(l.health, 2) for l in lands])
        # moneys2 = [p.money for p in ppl]
        # print("MEAN: " + str(np.mean(moneys2)) + '\n' + "STD: " + str(np.std(moneys2)))
        # print(np.array(moneys2) - np.array(moneys1))

        # result['final_ppl'] = [p.serialize(ppl) for p in res['ppl']]
        # moneys = np.array([x.money for x in res['ppl']])

        result['mean'] = res['mean'] - results['mean']
        result['STD'] = res['STD'] - results['STD']
        result['percentiles'] = res['percentiles']

        # result['need'] = res['need']
        # result['greed'] = res['greed']
        # result['env_con'] = res['env_con']

        result['deals'] = res['deals']
        
        result['deals_annuled'] = res['deals_annuled']
        result['lands_health'] = res['lands_health']
        result['type'] = type

        results['result'].append(result)

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
      loan_possible_index = np.where(np.array([p.money for p in sorted_ppl]) > 0.0)[0][0]
    except:
      # print(np.array([p.money for p in sorted_ppl]))
      continue

    for land in landz:
      worker_i = rng.integers(len(ppl)) - 1
      loaner_i = rng.integers(worker_i + 1, len(ppl))

      worker = sorted_ppl[worker_i]
      loaner = sorted_ppl[loaner_i]

      # Skip to the next one if loaner doesn't have enough money to lend
      deal = None
      if (type == "commerce"):
        deal = Commerce(t, loaner, worker, land, amount)
      if (type == "usury"):
        deal = Usury(t, loaner, worker, land, amount, r)
      
      if not deal.is_possible():
        # print('yo')
        continue
      deal.execute(ppls)

      if deal.annuled:
        #This is the case when the deal was annuled due to environmental reasons
        deals_annuled += 1
        land.health += (1 - land.health) / 4.0
      else:
        if deal.loss:
          pass
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
              # 'land': round(land.health, 2),
              'amount': amount, 
              'loss': deal.loss,
              # 'annuled' : deal.annuled,
          })

  result['ppl'] = ppls


  moneys = np.array([x.money for x in ppls])
  result['mean'] = np.mean(moneys)
  result['STD'] = np.std(moneys)

  result['deals'] = deals

  # result['need'] = np.mean(np.array([(x['loaner'][0]+x['worker'][0])/2 for x in deals]))
  # if result['need'] < 0.0: 
    # print(np.array([x['loaner'] for x in deals]))
  # result['greed'] = np.mean(np.array([(x['loaner'][1]+x['worker'][1])/2 for x in deals]))
  # result['env_con'] = np.mean(np.array([(x['loaner'][2]+x['worker'][2])/2 for x in deals]))
  result['percentiles'] = [np.percentile(moneys, q) for q in range(1,100,24)]

  result['deals_annuled'] = float(deals_annuled)
  result['lands_health'] = np.mean(np.array([l.health for l in landz]))

  return result

  
run()
      


# result = {}
# result['init_ppl'] = [p.serialize(ppl) for p in ppl]

# moneys1 = [p.money for p in ppl]
# print("MEAN: " + str(np.mean(moneys1)) + '\n' + "STD: " + str(np.std(moneys1)))

# commerce()
# print(str(deals_annuled) + ' deals annuled.')
# print([round(l.health, 2) for l in lands])
# moneys2 = [p.money for p in ppl]
# print("MEAN: " + str(np.mean(moneys2)) + '\n' + "STD: " + str(np.std(moneys2)))
# # print(np.array(moneys2) - np.array(moneys1))

# result['final_ppl'] = [p.serialize(ppl) for p in ppl]

# result['deals'] = deals
# result['deals_annuled'] = deals_annuled
# result['lands'] = [l.health for l in lands]
# result['type'] = 'commerce'
# result['ML'] = MAX_LOAD
# result['LCP'] = LOAN_CAP_RATIO
# result['N'] = N


# all_results = []
# with open('results.json', encoding='utf-8') as results:
#   all_results = json.load(results)

# all_results.append(result)
# with open('results.json', mode='w', encoding='utf-8') as results:
#   json.dump(all_results, results)

