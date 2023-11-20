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
    return self.amount > 0 and self.loaner.money > self.amount 

  def evaluate_deal(self, humans):
    thirst = (self.farmer.get_thirst(humans) +
              self.loaner.get_thirst(humans)) / 2.0
    
    # if thirst > self.land.health:
    #   return True
    
    if self.rng.random() < thirst:
      return True

    return False

  
class Commerce(Deal):

  def execute(self, humans):

    if self.loaner.money < self.amount:
      pass

    if self.evaluate_deal(humans):
      thirst_worker = self.farmer.get_thirst(humans)
      returns = self.land.work_on(self.farmer, thirst_worker)

      # 0 1 2 3 .. 10
      if returns == 0.0:
        self.loss = True

      # 10 - 10

      # 5
      # profit = revenue - expendiutre
      # share value share loss
      # 10 -> 20 -> 15 5
      # 10 -> 0 
      # 10 -> 5
      # EXPENDITURE 

      # -10-----10

      # 10 
      # -10 -> -5 -5 

      # 10 euros you give me 
      # 10 euros i make with it

      # delta = returns - self.amount
      # 5 
      self.farmer.receives(returns/2.0)
      self.loaner.receives(returns/2.0)

    else:
      self.annuled = True


class Usury(Deal):

  def __init__(self, id, loaner, farmer, land, amount, interest):
    Deal.__init__(self, id, loaner, farmer, land, amount)
    self.interest = interest
  
  # def evaluate_deal(self, humans):
  #   thirst = self.farmer.get_thirst(humans)
    
  #   # if thirst > self.land.health:
  #   #   return True
    
  #   if self.rng.random() < thirst:
  #     return True

  #   return False

  def execute(self, humans):

    if self.loaner.money < self.amount:
      pass

    if self.evaluate_deal(humans):

      thirst_worker = self.farmer.get_thirst(humans)
      returns = self.land.work_on(self.farmer, thirst_worker)
      
      self.farmer.receives(returns)

      self.farmer.pays(self.amount * self.interest)
      self.loaner.receives(self.amount * self.interest)

    else:
      self.annuled = True

