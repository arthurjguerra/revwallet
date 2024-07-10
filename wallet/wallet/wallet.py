class Wallet:
  def __init__(self, currency, initial_balance, owner):
    self.currency = currency
    self.balance = initial_balance
    self.owner = owner

  def check_balance(self):
    return self.balance
  
  def __str__(self):
    return f'Wallet of {self.owner} with balance of {self.balance} {self.currency}'