from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime

db = SQLAlchemy()


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def __repr__(self):
        return f"<User {self.username}>"

    def check_password(self, password):
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)


class Dispenser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    flow_volume = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)
    is_open = db.Column(db.Boolean, default=False)
    transactions = db.relationship("Transaction", back_populates="dispenser")

    def __init__(self, flow_volume, price):
        self.flow_volume = flow_volume
        self.price = price
        self.is_open = False

    def get_dispenser_info(self):
        return {
            "id": self.id,
            "flow_volume": self.flow_volume,
            "price": self.price,
            "is_open": self.is_open,
        }

    def get_dispenser_stats(self):
        transactions = self.transactions

        total_transactions = len(transactions)  # type: ignore

        dispenser_stats = {
            "dispenser_id": self.id,
            "flow_volume": self.flow_volume,
            "price": self.price,
            "is_open": self.is_open,
            "total_transactions": total_transactions,
            "total_amount": 0,
            "total_revenue": 0,
            "transactions": [],
        }

        total_amount = 0
        total_revenue = 0
        now = datetime.utcnow()

        for transaction in transactions:  # type: ignore
            amount, revenue = transaction.get_amount_and_revenue(now)

            total_amount += amount
            total_revenue += revenue
            transaction_info = {
                "transaction_id": transaction.id,
                "start_time": transaction.start_time.strftime("%Y-%m-%d %H:%M:%S"),
                "end_time": transaction.end_time.strftime("%Y-%m-%d %H:%M:%S")
                if transaction.end_time
                else None,
                "amount": amount,
                "revenue": revenue,
            }
            dispenser_stats["transactions"].append(transaction_info)

        dispenser_stats["total_amount"] = total_amount
        dispenser_stats["total_revenue"] = total_revenue

        return dispenser_stats


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dispenser_id = db.Column(db.Integer, db.ForeignKey("dispenser.id"), nullable=False)
    start_time = db.Column(db.TIMESTAMP, nullable=False)
    end_time = db.Column(db.TIMESTAMP, nullable=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    revenue = db.Column(db.Float, nullable=False, default=0.0)
    dispenser = db.relationship("Dispenser", back_populates="transactions")

    def __init__(
        self, dispenser_id, start_time=None, end_time=None, amount=0.0, revenue=0.0
    ):
        self.dispenser_id = dispenser_id
        self.start_time = start_time
        self.end_time = end_time
        self.amount = amount
        self.revenue = revenue

    def get_amount_and_revenue(self, end_time):
        if self.end_time is None:
            time_difference = end_time - self.start_time  # type: ignore
            amount = time_difference.total_seconds() * self.dispenser.flow_volume
            revenue = amount * self.dispenser.price

            return (amount, revenue)

        return (self.amount, self.revenue)
