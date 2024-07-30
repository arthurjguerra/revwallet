from . import db, logger

class Wallet(db.Model):
  __tablename__ = 'wallets'
  id = db.Column(db.Integer, primary_key=True,
                 nullable=False, autoincrement=True)
  currency = db.Column(db.String, nullable=False)
  balance = db.Column(db.Float, nullable=False)
  owner = db.Column(db.String, nullable=False)

  def __init__(self, currency, initial_balance, owner):
    logger.info(f'Creating wallet currency={currency}, balance={initial_balance}, owner={owner}')
    if initial_balance < 0:
      logger.error('Initial balance is negative')
      raise ValueError('Initial balance cannot be negative')

    self.currency = currency
    self.balance = initial_balance
    self.owner = owner

  def check_balance(self) -> str:
    logger.info(f'Checking balance of wallet {self.id} of {self.owner}')
    return f'{self.balance} {self.currency}'

  def withdraw(self, amount) -> None:
    logger.info(
        f'Withdrawing {amount} {self.currency} from wallet {self.id} of {self.owner}')
    if amount <= 0:
      logger.error('Amount to withdraw is negative')
      raise ValueError('Amount must be positive')
    if amount > self.balance:
      logger.error('Amount to withdraw is more than the balance')
      raise ValueError('Amount must be less than the balance')
    self.balance -= amount

  def deposit(self, amount) -> None:
    logger.info(
        f'Depositing {amount} {self.currency} to wallet {self.id} of {self.owner}')
    if amount < 0:
      logger.error('Amount to deposit is negative')
      raise ValueError('You cannot deposit a negative amount')
    if amount == 0:
      logger.error('Amount to deposit is 0')
      raise ValueError('You cannot deposit 0')
    if not isinstance(amount, (int, float)):
      logger.error('Amount to deposit is not an integer or float')
      raise TypeError('Amount must be a number')
    self.balance += amount

  def __str__(self):
    return f'Wallet of {self.owner} with balance of {self.balance} {self.currency}'

  def to_dict(self):
    return {
        'id': str(self.id),
        'currency': self.currency,
        'balance': self.balance,
        'owner': self.owner,
    }
