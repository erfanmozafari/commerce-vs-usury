import numpy as np



class Deal:

  def __init__(self, id, loaner, farmer, land, amount):
    self.id = id
    self.loaner = loaner
    self.farmer = farmer
    self.amount = amount
    self.land = land
    self.annuled = False
    self.loss = False
    self.rng = np.random.default_rng()

  def is_possible(self):
    return self.amount > 0

  def evaluate_deal(self, humans):
    thirst = (self.farmer.get_thirst(humans) +
              self.loaner.get_thirst(humans)) / 2.0
    
    if self.rng.random() < thirst:
      return True

    return False

  
class Commerce(Deal):

  def execute(self, humans):

    if self.loaner.money < self.amount:
      pass

    if self.evaluate_deal(humans):
      returns = self.land.work_on(self.farmer)
  
      if returns == 0.0:
        self.loss = True

      delta = returns - self.amount
      self.farmer.receives(delta/2.0)
      self.loaner.receives(delta/2.0)

    else:
      self.annuled = True


class Usury(Deal):

  def __init__(self, id, loaner, farmer, land, amount, interest):
    Deal.__init__(self, id, loaner, farmer, land, amount)
    self.interest = interest

  def execute(self, humans):

    if self.loaner.money < self.amount:
      pass

    if self.evaluate_deal(humans):
      self.loaner.pays(self.amount)
      self.farmer.receives(self.amount)

      returns = self.land.work_on(self.farmer)
      self.farmer.pays(self.amount)
      self.loaner.receives(self.amount)

      if returns == 0.0:
        self.loss = True

      self.farmer.receives(returns)
      self.farmer.pays(self.amount * self.interest)
      self.loaner.receives(self.amount * self.interest)

    else:
      self.annuled = True
