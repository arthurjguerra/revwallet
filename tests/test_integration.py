import unittest
from wallet import db, create_app
from wallet.wallet import Wallet
from uuid import UUID


class TestWalletIntegration(unittest.TestCase):
   
  def setUp(self):
    self.app = create_app(test_config={
      'SECRET_KEY': 'test',
      'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
      'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })
    self.app.testing = True
    self.client = self.app.test_client()

    with self.app.app_context():
        db.create_all()

  def tearDown(self):
      with self.app.app_context():
          db.drop_all()

  def test_integration_create_new_wallet(self):
    """Test the creation of a new wallet by checking the API response and the database."""

    response = self.client.post(
        '/wallet/new', 
        json={'initial_balance': '999.99', 'currency': 'EUR', 'owner': 'test user'}
    )

    response_id = response.get_json()['id']
    self.assertEqual(response.status_code, 201)
    self.assertEqual(response_id, str(UUID(response_id, version=4)))

    # Verify the wallet was persisted in the database
    with self.app.app_context():
      wallet = Wallet.query.filter_by(id=response_id).first()
      self.assertIsNotNone(wallet)
      self.assertEqual(wallet.id, response_id)

  def test_integration_deposit_money(self):
    """Test the creation of a new wallet by checking the API response and the database."""

    # create new wallet
    response_new_wallet = self.client.post(
      '/wallet/new',
      json={
        'initial_balance': '999.99',
        'currency': 'EUR', 
        'owner': 'test user'
      }
    )

    wallet_id = response_new_wallet.get_json()['id']

    response = self.client.post(
      '/wallet/deposit',
      json={
        'amount': '0.01',
        'id': wallet_id
      }
    )

    self.assertEqual(response.status_code, 200)

    # verify the wallet properties from the API
    api_wallet = response.get_json()
    self.assertIsNotNone(api_wallet)
    self.assertEqual(api_wallet['id'], wallet_id)
    self.assertEqual(api_wallet['balance'], 1000)
    self.assertEqual(api_wallet['currency'], "EUR")
    self.assertEqual(api_wallet['owner'], "test user")

    # Verify the wallet properties from the database
    with self.app.app_context():
      db_wallet = Wallet.query.filter_by(id=wallet_id).first()
      self.assertIsNotNone(db_wallet)
      self.assertEqual(db_wallet.id, wallet_id)
      self.assertEqual(db_wallet.balance, 1000)
