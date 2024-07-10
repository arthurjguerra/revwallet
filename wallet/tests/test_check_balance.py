import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency

class TestCheckBalance(unittest.TestCase):
  def setUp(self):
    self.test_wallet = Wallet(currency=Currency.EUR, initial_balance=1000, owner='Test User')
    
  def test_initial_balance(self):
    self.assertEqual(self.test_wallet.check_balance(), 1000)

  def test_wallet_to_str(self):
    self.assertEqual(str(self.test_wallet), 'Wallet of Test User with balance of 1000 EUR')
    

if __name__ == '__main__':
  unittest.main()
