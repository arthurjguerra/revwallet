# End of end test cases for the wallet API

import unittest
import requests


class TestWalletE2E(unittest.TestCase):

  def setUp(self):
    self.base_url = "http://127.0.0.1:8080"
    self.balance = 900.00
    self.currency = "EUR"
    self.owner = "test"

  def test_wallet_operations(self):
    # Create a wallet
    response = requests.post(f"{self.base_url}/wallet", json={
        "owner": self.owner,
        "initial_balance": self.balance,
        "currency": self.currency
    })
    self.assertEqual(response.status_code, 201)

    # Get the wallet from DB
    response = requests.get(f"{self.base_url}/wallet")
    self.assertEqual(response.status_code, 200)
    wallets = response.json()
    self.assertEqual(len(wallets), 1)

    wallet_id = wallets[0]["id"]

    # Check the balance of the wallet
    response = requests.get(f"{self.base_url}/wallet/balance/{wallet_id}")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(float(response.json()["balance"]), self.balance)

    # Deposit to the wallet
    response = requests.post(f"{self.base_url}/wallet/deposit", json={
        "id": wallet_id,
        "amount": "100.00"
    })
    self.assertEqual(response.status_code, 200)
    self.assertEqual(float(response.json()["balance"]), 1000.00)

    # Withdraw from the wallet
    response = requests.post(f"{self.base_url}/wallet/withdraw", json={
        "id": wallet_id,
        "amount": "50.00"
    })
    self.assertEqual(response.status_code, 200)
    self.assertEqual(float(response.json()["balance"]), 950.00)

    # Delete the wallet
    response = requests.delete(f"{self.base_url}/wallet/{wallet_id}")
    self.assertEqual(response.status_code, 204)

    # check if there is no wallet in DB after deletion
    response = requests.get(f"{self.base_url}/wallet")
    self.assertEqual(response.status_code, 200)
    wallets = response.json()
    self.assertEqual(len(wallets), 0)

    # Delete a wallet that doesn't exist
    response = requests.delete(f"{self.base_url}/wallet/{wallet_id}")
    self.assertEqual(response.status_code, 404)



if __name__ == '__main__':
  unittest.main()
