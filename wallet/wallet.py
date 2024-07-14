import uuid
from . import db

class Wallet(db.Model):
  __tablename__ = 'wallets'
  id = db.Column(db.String, primary_key=True, nullable=False)
  currency = db.Column(db.String, nullable=False)
  balance = db.Column(db.Float, nullable=False)
  owner = db.Column(db.String, nullable=False)

  def __init__(self, currency, initial_balance, owner):
    if initial_balance < 0:
      raise ValueError('Initial balance cannot be negative')

    self.id = str(uuid.uuid4())
    self.currency = currency
    self.balance = initial_balance
    self.owner = owner

  def check_balance(self) -> str:
    return f'{self.balance} {self.currency}'

  def withdrawal(self, amount) -> None:
    if amount <= 0:
      raise ValueError('Amount must be positive')
    if amount > self.balance:
      raise ValueError('Amount must be less than the balance')
    self.balance -= amount

  def deposit(self, amount) -> None:
    if amount < 0:
      raise ValueError('You cannot deposit a negative amount')
    self.balance += amount
  
  def __str__(self):
    return f'Wallet of {self.owner} with balance of {self.balance} {self.currency}'
  
  def to_dict(self):
    return {
      'id': self.id,
      'currency': self.currency,
      'balance': self.balance,
      'owner': self.owner,
    }
