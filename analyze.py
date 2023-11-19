import json
import numpy as np

results = []
with open('results.json', encoding='utf-8') as results:
  results = json.load(results)

  print(results['mean'])
  print(results['STD'])

  health_usury = 0.0
  mean_usury = 0.0
  std_usury = 0.0

  health_commerce = 0.0
  mean_commerce = 0.0
  mean_usury = 0.0

  iterations = results['result']

  commerce = list(filter(lambda iteration:iteration['type'] == 'commerce', iterations))
  usury = list(filter(lambda iteration:iteration['type'] == 'usury', iterations))

  print(len(commerce))
  print(len(usury))

  mean_moneys_commerce = np.mean(np.array([iteration['mean'] for iteration in commerce]))
  std_moneys_commerce = np.mean(np.array([iteration['STD'] for iteration in commerce]))
  land_health_commerce = np.mean(np.array([iteration['lands_health'] for iteration in commerce]))

  mean_moneys_usury = np.mean(np.array([iteration['mean'] for iteration in usury]))
  std_moneys_usury = np.mean(np.array([iteration['STD'] for iteration in usury]))
  land_health_usury = np.mean(np.array([iteration['lands_health'] for iteration in usury]))

#   mean_moneys_commerce /= (10**20)



  print('COMMERCE:', '\n' ,
    'MEAN : ' , mean_moneys_commerce, '\n' ,
    'STD : ', std_moneys_commerce, '\n' ,
    'HEALTH : ', land_health_commerce,
  )

  print('USURY:', '\n' ,
    'MEAN : ' , mean_moneys_usury, '\n' ,
    'STD : ', std_moneys_usury, '\n' ,
    'HEALTH : ', land_health_usury, 
  )


#   for iteration in results:
    
#     if iteration['type'] == 'commerce':
#         commerce.append((iteration['mean'], iteration['std'], ))
#     if iteration['type'] = 'usury':


