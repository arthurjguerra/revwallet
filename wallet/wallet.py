class Wallet:
  def __init__(self, currency, initial_balance, owner):
    if initial_balance < 0:
      raise ValueError('Initial balance cannot be negative')

    self.currency = currency
    self.balance = initial_balance
    self.owner = owner

  def check_balance(self):
    return self.balance

  def withdraw(self, amount):
    if amount <= 0:
      raise ValueError('Amount must be positive')
    if amount > self.balance:
      raise ValueError('Amount must be less than the balance')
    self.balance -= amount

  def deposit(self, amount):
    if amount < 0:
      raise ValueError('You cannot deposit a negative amount')
    self.balance += amount
  
  def __str__(self):
    return f'Wallet of {self.owner} with balance of {self.balance} {self.currency}'
