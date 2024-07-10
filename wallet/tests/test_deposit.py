import unittest
from wallet.wallet import Wallet
from wallet.currencies import Currency


class TestDeposit(unittest.TestCase):
  def setUp(self):
    self.test_wallet = Wallet(currency=Currency.EUR,
                              initial_balance=1000, owner='Test User')

  def test_deposit(self):
    pass


if __name__ == '__main__':
  unittest.main()
