import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency


class TestDeposit(unittest.TestCase):
  def setUp(self):
    self.test_wallet = Wallet(currency=Currency.EUR,
                              initial_balance=1000, owner='Test User')

  def test_deposit(self):
    self.test_wallet.deposit(500)
    self.assertEqual(self.test_wallet.check_balance(), '1500 EUR')

  def test_deposit_negative(self):
    with self.assertRaises(ValueError):
      self.test_wallet.deposit(-500)

  def test_deposit_zero(self):
    with self.assertRaises(ValueError):
      self.test_wallet.deposit(0)
      self.assertEqual(self.test_wallet.check_balance(), '1000 EUR')

  def test_deposit_multiple_times(self):
    self.test_wallet.deposit(200)
    self.test_wallet.deposit(300)
    self.assertEqual(self.test_wallet.check_balance(), '1500 EUR')

  def test_deposit_large_amount(self):
    self.test_wallet.deposit(1000000)
    self.assertEqual(self.test_wallet.check_balance(), '1001000 EUR')

  def test_deposit_float_amount(self):
    self.test_wallet.deposit(123.45)
    self.assertEqual(self.test_wallet.check_balance(), '1123.45 EUR')

  def test_deposit_invalid_amount(self):
    with self.assertRaises(TypeError):
      self.test_wallet.deposit('500')


if __name__ == '__main__':
  unittest.main()
