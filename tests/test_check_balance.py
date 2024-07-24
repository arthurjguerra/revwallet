import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency

class TestCheckBalance(unittest.TestCase):
  def setUp(self):
    self.test_wallet = Wallet(currency=Currency.EUR, initial_balance=1000, owner='Test User')
    
  def test_initial_balance(self):
    self.assertEqual(self.test_wallet.check_balance(), '1000 EUR')

  def test_check_balance_after_deposit(self):
    self.test_wallet.deposit(500)
    self.assertEqual(self.test_wallet.check_balance(), '1500 EUR')

  def test_check_balance_after_withdraw(self):
    self.test_wallet.withdraw(200.50)
    self.assertEqual(self.test_wallet.check_balance(), '799.5 EUR')

  def test_check_balance_after_multiple_transactions(self):
      self.test_wallet.withdraw(100)
      self.test_wallet.deposit(155.55)
      self.assertEqual(self.test_wallet.check_balance(), '1055.55 EUR')

  def test_check_balance_after_invalid_deposit(self):
    try:
      self.test_wallet.deposit(-100)
    except Exception:
      pass
    finally:
      self.assertEqual(self.test_wallet.check_balance(), '1000 EUR')

  def test_check_balance_after_invalid_withdraw(self):
    try:
      self.test_wallet.withdraw(2222222)
    except Exception:
      pass
    finally:
      self.assertEqual(self.test_wallet.check_balance(), '1000 EUR')

  def test_check_balance_after_multiple_withdrawals(self):
    self.test_wallet.withdraw(100)
    self.test_wallet.withdraw(50)
    self.assertEqual(self.test_wallet.check_balance(), '850 EUR')

  def test_check_balance_after_multiple_deposits(self):
    self.test_wallet.deposit(200)
    self.test_wallet.deposit(300)
    self.assertEqual(self.test_wallet.check_balance(), '1500 EUR')

  def test_check_balance_after_invalid_withdraw_and_deposit(self):
    self.test_wallet.withdraw(1000)
    try:
      self.test_wallet.deposit(-200)
    except Exception:
      pass

    self.assertEqual(self.test_wallet.check_balance(), '0 EUR')

  def test_check_balance_after_multiple_withdrawals_and_deposits(self):
    self.test_wallet.withdraw(100)
    self.test_wallet.withdraw(50)
    self.test_wallet.deposit(200)
    self.test_wallet.deposit(300)
    self.assertEqual(self.test_wallet.check_balance(), '1350 EUR')

  def test_check_balance_after_zero_balance(self):
    self.test_wallet.withdraw(1000)
    self.assertEqual(self.test_wallet.check_balance(), '0 EUR')

  def test_check_balance_after_large_deposit(self):
    self.test_wallet.deposit(1000000)
    self.assertEqual(self.test_wallet.check_balance(), '1001000 EUR')

  def test_check_balance_after_large_withdrawal(self):
    self.test_wallet.withdraw(1000)
    self.test_wallet.deposit(1000000)
    self.test_wallet.withdraw(999999)
    self.assertEqual(self.test_wallet.check_balance(), '1 EUR')
    

if __name__ == '__main__':
  unittest.main()
