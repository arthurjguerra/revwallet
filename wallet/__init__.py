import os

from flask import Flask, request
from wallet.currencies import Currency
from wallet.wallet import Wallet

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'wallet.sqlite'),
    )
    wallet = Wallet(currency=Currency.EUR, initial_balance=1000, owner='My User')

    if test_config:
        # test configuration
        app.config.from_mapping(test_config)
    else:
        # production configuration
        app.config.from_pyfile('config.py', silent=True)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        print(f'{app.instance_path} directory already exists.')

    @app.route('/')
    def index():
        return 'Welcome to RevWallet'

    @app.route('/balance', methods=['GET'])
    def check_balance():
        data = request.get_json()
        id = data.get('id')
        return f'Balance of Wallet {id} is {wallet.check_balance()}'
    
    @app.route('/deposit', methods=['POST'])
    def deposit():
        data = request.get_json()
        id = data.get('id')
        amount = float(data.get('amount'))
        wallet.deposit(amount)
        return f'Deposit {amount}'
    
    @app.route('/withdrawal', methods=['POST'])
    def withdraw():
        data = request.get_json()
        id = data.get('id')
        amount = float(data.get('amount'))
        wallet.withdrawal(amount)
        return f'Withdrawal {amount}'

    return app
