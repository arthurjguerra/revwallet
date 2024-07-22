# End of end test cases for the wallet API

import unittest
import requests


class TestWalletE2E(unittest.TestCase):

  def setUp(self):
    self.self.base_url = "http://127.0.0.1:5000"
    self.balance = "900.00"
    self.currency = "EUR"
    self.owner = "test"

  def test_create_wallet(self):
    response = requests.post(f"{self.base_url}/wallet/new", json={
      "owner": self.owner,
      "initial_balance": self.balance,
      "currency": self.currency
    })
    self.assertEqual(response.status_code, 201)

  def test_get_wallets(self):
      response = requests.get(f"{self.base_url}/wallet")
      self.assertEqual(response.status_code, 200)
      wallets = response.json()
      self.assertEqual(len(wallets), 1)

  def test_get_balance(self):
      response = requests.get(f"{self.base_url}/wallet")
      wallets = response.json()
      wallet_id = wallets[0]["id"]
      response = requests.get(f"{self.base_url}/wallet/balance", params={"id": wallet_id})
      self.assertEqual(response.status_code, 200)
      balance = response.json()["balance"]
      self.assertEqual(balance, self.balance)

  def test_deposit(self):
    response = requests.get(f"{self.base_url}/wallet")
    wallets = response.json()
    wallet_id = wallets[0]["id"]
    response = requests.post(f"{self.base_url}/wallet/deposit", json={
        "id": wallet_id,
        "amount": "100.00"
    })
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()["balance"], 1000.00)

    response = requests.get(
        f"{self.base_url}/wallet/balance", params={"id": wallet_id})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()["balance"], 1000.00)

  def test_withdrawal(self):
    response = requests.get(f"{self.base_url}/wallet")
    wallets = response.json()
    wallet_id = wallets[0]["id"]
    response = requests.post(f"{self.base_url}/wallet/withdrawal", json={
        "id": wallet_id,
        "amount": "50.00"
    })
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()["balance"], 950.00)

    response = requests.get(
        f"{self.base_url}/wallet/balance", params={"id": wallet_id})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json()["balance"], 950.00)
     
