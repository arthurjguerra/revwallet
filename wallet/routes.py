from flask import Blueprint, request, jsonify
from .wallet import Wallet, db

bp = Blueprint('wallet', __name__)

@bp.route('/')
def index():
    with db.session() as session:
        wallets = session.query(Wallet).all()
        return jsonify([wallet.to_dict() for wallet in wallets])

@bp.route('/new', methods=['POST'])
def create_new_wallet():
    data = request.get_json()
    initial_balance = float(data.get('initial_balance'))
    currency = data.get('currency')
    owner = data.get('owner')

    with db.session() as session:
        new_wallet = Wallet(currency=currency, initial_balance=initial_balance, owner=owner)
        session.add(new_wallet)
        session.commit()
        return jsonify({'id': new_wallet.id}), 201

@bp.route('/balance', methods=['GET'])
def check_balance():
    data = request.get_json()
    id = data.get('id')

    with db.session() as session:
        wallet = session.get(Wallet, id)

        if not wallet:
            return f'Wallet {id} not found', 404

        return jsonify(wallet.to_dict())

@bp.route('/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    id = data.get('id')
    amount = float(data.get('amount'))
    
    with db.session() as session:
        wallet = session.get(Wallet, id)

        if not wallet:
            return f'Wallet {id} not found', 404

        wallet.deposit(amount)
        session.commit()
        return jsonify(wallet.to_dict())

@bp.route('/withdrawal', methods=['POST'])
def withdraw():
    data = request.get_json()
    id = data.get('id')
    amount = float(data.get('amount'))

    with db.session() as session:
        wallet = session.get(Wallet, id)

        if not wallet:
            return f'Wallet {id} not found', 404

        wallet.withdrawal(amount)
        session.commit()
        return jsonify(wallet.to_dict())
