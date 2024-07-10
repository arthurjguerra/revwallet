import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency


class TestDeposit(unittest.TestCase):
  def setUp(self):
    self.test_wallet = Wallet(currency=Currency.EUR,
                              initial_balance=1000, owner='Test User')

  def test_deposit(self):
    self.test_wallet.deposit(500)
    self.assertEqual(self.test_wallet.check_balance(), 1500)

  def test_deposit_negative(self):
    with self.assertRaises(ValueError):
      self.test_wallet.deposit(-500)


if __name__ == '__main__':
  unittest.main()
