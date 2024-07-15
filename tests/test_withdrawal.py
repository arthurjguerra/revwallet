import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency

class TestWithdrawal(unittest.TestCase):
  def setUp(self):
    self.wallet = Wallet(currency=Currency.EUR, initial_balance=1000, owner='Test User')

  def test_withdraw(self):
    self.wallet.withdrawal(500)
    self.assertEqual(self.wallet.balance, 500)

  def test_withdraw_amount_bigger_than_balance(self):
    with self.assertRaises(ValueError):
      self.wallet.withdrawal(200000000)

  def test_withdraw_negative_amount(self):
    with self.assertRaises(ValueError):
      self.wallet.withdrawal(-50)

  def test_withdraw_zero_amount(self):
    with self.assertRaises(ValueError):
      self.wallet.withdrawal(0)

  def test_withdraw_multiple_times(self):
    self.wallet.withdrawal(300)
    self.wallet.withdrawal(200)
    self.assertEqual(self.wallet.balance, 500)

if __name__ == '__main__':
  unittest.main()
