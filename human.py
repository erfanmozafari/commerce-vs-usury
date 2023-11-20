import numpy as np


class Human:

  def __init__(self, id, money, env_con):
    self.id = id
    self.money = money
    self.env_con = env_con
    self.rng = np.random.default_rng()

  def receives(self, money):
    self.money += money

  def pays(self, money):
    self.money -= money

  def get_need_greed(self, humans):
    humans = np.array([h.money for h in humans])
    humans = np.sort(humans)

    N = len(humans)
    mean = np.mean(humans)
    mean_i = np.argmin(np.array([abs(x - mean) for x in humans]))
    bottom = humans[0]
    median = humans[N//2]
    median_i = N//2
    top = humans[-1]
    this_i = np.nonzero(humans == self.money)[0][-1]

    mid_val = (median+mean)/2.0
    mid_val_i = np.argmin(np.array([abs(x - mid_val) for x in humans]))

    # 40
    # 50
    # -20    -10      30    40   

    n1, n2 = 0.0, 0.0
    g1, g2 = 0.0, 0.0

    
    # if self.money < mid_val:
    #   if (mid_val - bottom) > 1.0:
    #     n1 = (mid_val - self.money) / (mid_val - bottom)
    #     n2 = 1- (mid_val_i-this_i) / mid_val_i

    if self.money < mean:
      if (mean - bottom) > 1.0:
        n1 = (mean - self.money) / (mean - bottom)
        n2 = 1- (mean_i-this_i) / mean_i

    # n1 = (min(self.money, mid_val) -      / float(mid_val - bottom)
    # n2 = min(this_i, mid_val_i)       / float(mid_val_i)

    #         50    70        100
    # 0       30    50        100
    g1 = 1 - (top-self.money) / (top-bottom)
    g2 = this_i / float(N)
    # if self.money > mid_val:
    #   if (top - mid_val) > 1.0:
    #     g1 = 1 - (top-self.money)/ float(top-mid_val)
    #     g2 = 1 - (N-this_i) / float(N-median_i)
    # g1 = max(0, self.money - mid_val) / float(top-mid_val)
    # g2 = max(0, this_i-mid_val_i)     / float(N - mid_val_i)

    need = (n1 + n2) / 2.0
    greed = (g1 + g2) / 2.0

    # if (need) < 0.0:
    #   print(n1, n2)

    return (need, greed)

  def get_thirst(self, humans):
    need, greed = self.get_need_greed(humans)
    # env_disregard = (1 - self.env_con)

    return (need + greed)/2.0


  def serialize(self, humans):
    need, greed = self.get_need_greed(humans)
    return {
        'id': self.id,
        'money': round(self.money, 2),
        'need': round(need, 2),
        'greed': round(greed, 2),
        # 'env_con': round(self.env_con, 2)
    }
