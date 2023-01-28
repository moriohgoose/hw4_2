from migrate import data_to_db
from models import User, Order, Offer
from flask import jsonify, Flask, request, abort
from init_db import db
from flask_sqlalchemy import SQLAlchemy
from migrate import data_to_db
from config import Config


app = Flask(__name__)


@app.route('/users/', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        try:
            users = db.session.query(User).all()
            return jsonify([user.serialize() for user in users])
        except Exception as e:
            return f'{e}'
    elif request.method == 'POST':
        data = request.json
        db.session.add(User(**data))
        db.session.commit()

        return jsonify(code=200)


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(user_id):
    if request.method == 'GET':
        try:
            user = db.session.query(User).filter(User.id == user_id).first()
            return jsonify(user.serialize())
        except Exception as e:
            return f'{e}'

    elif request.method == 'PUT':
        user = db.session.query(User).filter(User.id == user_id).first()

        if user is None:
            abort(404)

        db.session.query(User).filter(User.id == user_id).update(request.json)
        db.session.commit()
        return jsonify(code=200)

    elif request.method == 'DELETE':
        count = db.session.query(User).filter(User.id == user_id).delete
        db.session.commit()
        if not count:
            abort(404)
        return jsonify(code=200)


@app.route('/orders/', methods=['GET'])
def get_orders():
    try:
        orders = db.session.query(Order).all()
        return jsonify([order.serialize() for order in orders])
    except Exception as e:
        return f'{e}'


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    try:
        order = db.session.query(Order).filter(Order.id == order_id).first()
        return jsonify(order.serialize())
    except Exception as e:
        return f'{e}'


@app.route('/offers/', methods=['GET'])
def get_offers():
    try:
        offers = db.session.query(Offer).all()
        return jsonify([offer.serialize() for offer in offers])
    except Exception as e:
        return f'{e}'


@app.route('/offers/<int:offer_id>', methods=['GET'])
def get_offer(offer_id):
    try:
        offer = db.session.query(Offer).filter(Offer.id == offer_id).first()
        return jsonify(offer.serialize())
    except Exception as e:
        return f'{e}'


if __name__ == '__main__':
    app.config.from_object(Config())

    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        data_to_db()

    app.run(port=5000, debug=True)

