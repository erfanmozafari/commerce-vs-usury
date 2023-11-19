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
    # print(humans)
    this_i = np.where(humans==self.money)[0][-1]
    # this_i = humans.index(self.money)
    top = humans[-1]

    n1 = 1 - min(mean, self.money)/mean
    n2 = 1 - min(mean_i, this_i)/mean_i
    n2 = n1

    g1 = self.money / top
    g2 = this_i / N-1
    g2 = g1

    need = (n1 + n2) / 2.0
    greed = (g1 + g2) / 2.0

    return (need, greed)

  def get_thirst(self, humans):
    need, greed = self.get_need_greed(humans)
    # env_disregard = (1 - self.env_con)

    return (need + greed) / 2.0


  def serialize(self, humans):
    need, greed = self.get_need_greed(humans)
    return {
        'id': self.id,
        'money': round(self.money, 2),
        'need': round(need, 2),
        'greed': round(greed, 2),
        'env_con': round(self.env_con, 2)
    }
