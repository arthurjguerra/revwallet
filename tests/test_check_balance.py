import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency

class TestCheckBalance(unittest.TestCase):
  def setUp(self):
    self.test_wallet = Wallet(currency=Currency.EUR, initial_balance=1000, owner='Test User')
    
  def test_initial_balance(self):
    self.assertEqual(self.test_wallet.check_balance(), '1000 EUR')

  def test_deposit(self):
    self.test_wallet.deposit(500)
    self.assertEqual(self.test_wallet.check_balance(), '1500 EUR')

  def test_withdraw(self):
    self.test_wallet.withdraw(200.50)
    self.assertEqual(self.test_wallet.check_balance(), '799.5 EUR')

  def test_multiple_transactions(self):
      self.test_wallet.withdraw(100)
      self.test_wallet.deposit(155.55)
      self.assertEqual(self.test_wallet.check_balance(), '1055.55 EUR')
    

if __name__ == '__main__':
  unittest.main()
