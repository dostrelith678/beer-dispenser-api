import pytest

from app.models import Dispenser, Transaction
from datetime import datetime, timedelta


@pytest.mark.usefixtures("test_setup", "test_teardown")
class TestStatistics:
    def test_get_statistics_no_transactions(self, test_setup):
        client, db, test_jwt = test_setup

        dispenser1 = Dispenser(flow_volume=0.5, price=2.0)
        dispenser2 = Dispenser(flow_volume=0.7, price=3.0)
        db.session.add_all([dispenser1, dispenser2])
        db.session.commit()

        headers = {"Authorization": f"Bearer {test_jwt}"}
        response = client.get("/api/statistics", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert isinstance(data, list)
        assert len(data) == 2

        for item in data:
            assert "dispenser_id" in item
            assert "transactions" in item
            assert isinstance(item["transactions"], list)
            assert len(item["transactions"]) == 0

    def test_get_statistics_existing_transactions(self, test_setup):
        client, db, test_jwt = test_setup

        dispenser1 = Dispenser(flow_volume=1.0, price=2.0)
        dispenser2 = Dispenser(flow_volume=2.0, price=3.0)
        db.session.add_all([dispenser1, dispenser2])
        db.session.flush()

        transaction1 = Transaction(
            dispenser_id=dispenser1.id,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(seconds=5),
            amount=5.0,
            revenue=10.0,
        )
        transaction2 = Transaction(
            dispenser_id=dispenser2.id,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(seconds=5),
            amount=10.0,
            revenue=30.0,
        )
        transaction3 = Transaction(
            dispenser_id=dispenser2.id,
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(seconds=5),
            amount=10.0,
            revenue=30.0,
        )
        db.session.add_all([transaction1, transaction2, transaction3])

        db.session.commit()

        headers = {"Authorization": f"Bearer {test_jwt}"}
        response = client.get("/api/statistics", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert isinstance(data, list)
        assert len(data) == 2

        for item in data:
            assert "dispenser_id" in item
            assert "total_amount" in item
            assert "total_revenue" in item
            assert "total_transactions" in item
            assert "transactions" in item
            assert isinstance(item["transactions"], list)

        assert data[0]["is_open"] == False
        assert data[0]["total_amount"] == 5.0
        assert data[0]["total_revenue"] == 10.0
        assert data[0]["total_transactions"] == 1

        assert data[1]["is_open"] == False
        assert data[1]["total_amount"] == 20.0
        assert data[1]["total_revenue"] == 60.0
        assert data[1]["total_transactions"] == 2

    def test_get_statistics_some_dispensers_open(self, test_setup):
        client, db, test_jwt = test_setup

        dispenser1 = Dispenser(flow_volume=0.5, price=2.0)
        dispenser2 = Dispenser(flow_volume=0.7, price=3.0)
        db.session.add_all([dispenser1, dispenser2])
        db.session.commit()

        response = client.post(f"api/dispenser/{dispenser1.id}/open")

        headers = {"Authorization": f"Bearer {test_jwt}"}
        response = client.get("/api/statistics", headers=headers)
        assert response.status_code == 200
        data = response.json
        assert isinstance(data, list)
        assert len(data) == 2

        for item in data:
            assert "dispenser_id" in item
            assert "total_amount" in item
            assert "total_revenue" in item
            assert "is_open" in item
            assert "total_transactions" in item
            assert "transactions" in item
            assert isinstance(item["transactions"], list)

        assert data[0]["is_open"] == True
        assert data[0]["total_amount"] > 0.0
        assert data[0]["total_revenue"] > 0.0
        assert data[0]["total_transactions"] == 1

        assert data[1]["is_open"] == False
        assert data[1]["total_amount"] == 0.0
        assert data[1]["total_revenue"] == 0.0
        assert data[1]["total_transactions"] == 0

    def test_get_statistics_by_dispenser_id(self, test_setup):
        client, db, test_jwt = test_setup

        dispenser1 = Dispenser(flow_volume=0.5, price=2.0)
        dispenser2 = Dispenser(flow_volume=0.7, price=3.0)
        db.session.add_all([dispenser1, dispenser2])
        db.session.commit()

        response = client.post(f"api/dispenser/{dispenser1.id}/open")

        headers = {"Authorization": f"Bearer {test_jwt}"}
        response = client.get(f"/api/statistics/{dispenser1.id}", headers=headers)
        assert response.status_code == 200
        data = response.json

        assert data["is_open"] == True
        assert data["total_amount"] > 0.0
        assert data["total_revenue"] > 0.0
        assert data["total_transactions"] == 1
        assert "transactions" in data
