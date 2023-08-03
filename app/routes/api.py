from flask import Blueprint, request, jsonify
from app.models import db, Dispenser, Transaction
from datetime import datetime
from flask_jwt_extended import jwt_required

bp = Blueprint("api", __name__)


@bp.route("/dispenser", methods=["POST"])
@jwt_required()
def create_dispenser():
    data = request.get_json()
    flow_volume = data.get("flow_volume")
    price = data.get("price")
    if flow_volume is None or price is None:
        return jsonify({"message": "Flow volume and price are required"}), 400

    try:
        new_dispenser = Dispenser(flow_volume=flow_volume, price=price)
        db.session.add(new_dispenser)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": new_dispenser.id,
                    "flow_volume": new_dispenser.flow_volume,
                    "price": new_dispenser.price,
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error creating dispenser: {e}"}), 500


@bp.route("/dispenser/<int:dispenser_id>", methods=["GET"])
def get_dispenser_info_by_id(dispenser_id):
    dispenser = db.session.get(Dispenser, dispenser_id)

    if not dispenser:
        return jsonify({"message": "Dispenser not found"}), 404

    dispenser_info = dispenser.get_dispenser_info()

    return jsonify(dispenser_info), 200


@bp.route("/dispenser", methods=["GET"])
def get_all_dispenser_info():
    dispensers = Dispenser.query.all()

    dispenser_info = [dispenser.get_dispenser_info() for dispenser in dispensers]

    return jsonify(dispenser_info), 200


@bp.route("/dispenser/<int:dispenser_id>/open", methods=["POST"])
def open_dispenser(dispenser_id):
    dispenser = db.session.get(Dispenser, dispenser_id)

    if not dispenser:
        return jsonify({"message": "Dispenser not found"}), 404

    if dispenser.is_open:
        return jsonify({"message": "Dispenser is already open"}), 400

    try:
        new_transaction = Transaction(
            dispenser_id=dispenser_id, start_time=datetime.utcnow()
        )
        db.session.add(new_transaction)
        dispenser.is_open = True
        db.session.commit()

        return jsonify({"message": "Dispenser opened successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error opening dispenser: {e}"}), 500


@bp.route("/dispenser/<int:dispenser_id>/close", methods=["POST"])
def close_dispenser(dispenser_id):
    dispenser = db.session.get(Dispenser, dispenser_id)

    if not dispenser:
        return jsonify({"message": "Dispenser not found"}), 404

    if not dispenser.is_open:
        return jsonify({"message": "Dispenser is already closed"}), 400

    try:
        last_transaction = (
            Transaction.query.filter_by(dispenser_id=dispenser_id, end_time=None)
            .order_by(Transaction.start_time.desc())  # type: ignore
            .first()
        )

        if not last_transaction:
            return jsonify({"message": "No open transaction found"}), 500

        end_time = datetime.utcnow()

        amount, revenue = last_transaction.get_amount_and_revenue(end_time)

        last_transaction.amount = amount
        last_transaction.revenue = revenue
        last_transaction.end_time = end_time
        dispenser.is_open = False
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Dispenser closed successfully",
                    "amount": amount,
                    "cost": revenue,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": f"Error closing dispenser: {e}"}), 500


@bp.route("/statistics/<int:dispenser_id>", methods=["GET"])
@jwt_required()
def get_dispenser_stats_by_id(dispenser_id):
    dispenser = db.session.get(Dispenser, dispenser_id)

    if not dispenser:
        return jsonify({"message": "Dispenser not found"}), 404

    dispenser_stats = dispenser.get_dispenser_stats()

    return jsonify(dispenser_stats), 200


@bp.route("/statistics", methods=["GET"])
@jwt_required()
def get_all_dispenser_stats():
    statistics = []
    dispensers = Dispenser.query.all()

    for dispenser in dispensers:
        dispenser_stats = dispenser.get_dispenser_stats()

        statistics.append(dispenser_stats)

    return jsonify(statistics), 200
