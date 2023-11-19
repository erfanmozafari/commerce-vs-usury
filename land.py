import numpy as np

class Land:

  def __init__(self, id, MAX_CAP):
    self.id = id
    self.health = 1.0
    self.max_profit = MAX_CAP
    self.rng = np.random.default_rng()

  def did_suceed(self):
    return 1 if self.rng.random() >= 0.1 else 0
  
  def work_on(self, worker):
    R = self.health * self.max_profit * self.did_suceed()
    self.health /= 2.0
    return R
