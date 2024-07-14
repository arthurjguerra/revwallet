from flask import Blueprint, request, jsonify
from .wallet import Wallet, db

bp = Blueprint('wallet', __name__)

@bp.route('/')
def index():
    wallets = Wallet.query.all()
    jsonify([wallet.to_dict() for wallet in wallets])
    return jsonify([wallet.to_dict() for wallet in wallets])

@bp.route('/wallet', methods=['POST'])
def create_new_wallet():
    data = request.get_json()
    initial_balance = float(data.get('initial_balance'))
    currency = data.get('currency')
    owner = data.get('owner')
    new_wallet = Wallet(currency=currency, initial_balance=initial_balance, owner=owner)
    db.session.add(new_wallet)
    db.session.commit()
    return str(new_wallet.id)

@bp.route('/balance', methods=['GET'])
def check_balance():
    data = request.get_json()
    id = data.get('id')
    wallet = Wallet.query.get(id)
    if wallet:
        return f'{wallet}'
    else:
        return f'Wallet {id} not found', 404

@bp.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    id = data.get('id')
    amount = float(data.get('amount'))
    wallet = Wallet.query.get(id)
    if wallet:
        wallet.deposit(amount)
        db.session.commit()
        return f'Deposit {amount}'
    else:
        return f'Wallet {id} not found', 404

@bp.route('/withdrawal', methods=['POST'])
def withdraw():
    data = request.get_json()
    id = data.get('id')
    amount = float(data.get('amount'))
    wallet = Wallet.query.get(id)
    if wallet:
        wallet.withdrawal(amount)
        db.session.commit()
        return f'Withdrawal {amount}'
    else:
        return f'Wallet {id} not found', 404
