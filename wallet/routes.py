from flask import Blueprint, request, jsonify
from .wallet import Wallet, db, logger

bp = Blueprint('wallet', __name__)

@bp.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    if request.method == 'GET':
        logger.info('Request to get all wallets from DB')
        with db.session() as session:
            wallets = session.query(Wallet).all()
            return jsonify([wallet.to_dict() for wallet in wallets])
    elif request.method == 'POST':
        logger.info('Request to create a new wallet')
        data = request.get_json()
        initial_balance = float(data.get('initial_balance'))
        currency = data.get('currency')
        owner = data.get('owner')

        with db.session() as session:
            new_wallet = Wallet(currency=currency, initial_balance=initial_balance, owner=owner)
            session.add(new_wallet)
            session.commit()
            return jsonify({'id': new_wallet.id}), 201


@bp.route("/<id>", methods=["DELETE"])
def delete(id):
    logger.info(f"Wallet ID to delete: {id}")
    with db.session() as session:
        wallet = session.get(Wallet, id)
        if wallet:
            session.delete(wallet)
            session.commit()
            return '', 204
        else:
            return jsonify({'error': f'Could not delete Wallet: id {id} not found'}), 404

@bp.route('/balance/<int:id>', methods=['GET'])
def check_balance(id):
    logger.info(f'Request to check balance of wallet {id}')
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

    logger.info(f'Request to deposit {amount} to wallet {id}')
    
    with db.session() as session:
        wallet = session.get(Wallet, id)

        if not wallet:
            return f'Wallet {id} not found', 404

        wallet.deposit(amount)
        session.commit()
        return jsonify(wallet.to_dict())

@bp.route('/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    id = data.get('id')
    amount = float(data.get('amount'))

    logger.info(f'Request to withdraw {amount} from wallet {id}')

    with db.session() as session:
        wallet = session.get(Wallet, id)

        if not wallet:
            return f'Wallet {id} not found', 404

        wallet.withdraw(amount)
        session.commit()
        return jsonify(wallet.to_dict())
