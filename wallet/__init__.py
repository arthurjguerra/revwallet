import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'wallet.sqlite'),
    )

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

    @app.route('/balance/<int:account_id>', methods=['GET'])
    def check_balance(account_id):
        return f'Check balance of {account_id}'
    
    @app.route('/deposit/<float:amount>', methods=['POST'])
    def deposit(amount):
        return f'Deposit {amount}'
    
    @app.route('/withdrawal/<float:amount>', methods=['POST'])
    def withdraw(amount):
        return f'Withdraw {amount}'

    return app
