import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency

class TestWithdraw(unittest.TestCase):
  def setUp(self):
    self.wallet = Wallet(currency=Currency.EUR, initial_balance=1000, owner='Test User')

  def test_withdraw(self):
    self.wallet.withdraw(500)
    self.assertEqual(self.wallet.balance, 500)

  def test_withdraw_amount_bigger_than_balance(self):
    with self.assertRaises(ValueError):
      self.wallet.withdraw(200000000)

  def test_withdraw_negative_amount(self):
    with self.assertRaises(ValueError):
      self.wallet.withdraw(-50)

  def test_withdraw_zero_amount(self):
    with self.assertRaises(ValueError):
      self.wallet.withdraw(0)

  def test_withdraw_multiple_times(self):
    self.wallet.withdraw(300)
    self.wallet.withdraw(200)
    self.assertEqual(self.wallet.balance, 500)

  def test_withdraw_multiple_times_with_insufficient_balance(self):
    with self.assertRaises(ValueError):
      self.wallet.withdraw(1000)
      self.wallet.withdraw(1)

  def test_withdraw_fractional_amount(self):
    self.wallet.withdraw(0.5)
    self.assertEqual(self.wallet.balance, 999.5)

if __name__ == '__main__':
  unittest.main()
