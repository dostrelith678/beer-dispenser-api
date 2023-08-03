import pytest

from app.models import Dispenser, Transaction
from datetime import datetime


@pytest.mark.usefixtures("test_setup", "test_teardown")
class TestDispenser:
    def test_create_valid_dispenser_with_valid_auth(self, test_setup):
        client, _, test_jwt = test_setup

        headers = {"Authorization": f"Bearer {test_jwt}"}
        response = client.post(
            "api/dispenser", headers=headers, json={"flow_volume": 0.5, "price": 2.0}
        )
        assert response.status_code == 201

        dispenser = Dispenser.query.first()
        assert dispenser is not None
        assert dispenser.flow_volume == 0.5
        assert dispenser.price == 2.0

    def test_create_valid_dispenser_with_invalid_auth(self, test_setup):
        client, _, _ = test_setup

        response = client.post("api/dispenser", json={"flow_volume": 0.5, "price": 2.0})
        assert response.status_code == 401

        dispenser = Dispenser.query.first()
        assert dispenser is None

    def test_create_invalid_dispenser(self, test_setup):
        client, _, test_jwt = test_setup
        headers = {"Authorization": f"Bearer {test_jwt}"}
        response = client.post(
            "api/dispenser",
            headers=headers,
            json={
                "price": 0.5,  # Missing the 'flow_volume' field
            },
        )
        assert response.status_code == 400
        assert "Flow volume and price are required" in response.json["message"]

        response = client.post(
            "api/dispenser",
            headers=headers,
            json={
                "flow_volume": 0.5,  # Missing the 'price' field
            },
        )
        assert response.status_code == 400
        assert "Flow volume and price are required" in response.json["message"]

    def test_get_dispenser_by_id_tap_closed(self, test_setup):
        client, db, _ = test_setup

        dispenser = Dispenser(flow_volume=0.5, price=2.0)
        db.session.add(dispenser)
        db.session.commit()

        response = client.get(f"api/dispenser/{dispenser.id}")
        assert response.status_code == 200
        data = response.json
        assert "id" in data
        assert "flow_volume" in data
        assert "price" in data
        assert "is_open" in data

        assert data["id"] == dispenser.id
        assert data["flow_volume"] == 0.5
        assert data["price"] == 2.0
        assert data["is_open"] == False

    def test_get_dispenser_by_id_tap_open(self, test_setup):
        client, db, _ = test_setup

        dispenser = Dispenser(flow_volume=0.5, price=2.0)
        db.session.add(dispenser)
        db.session.commit()

        response = client.post(f"api/dispenser/{dispenser.id}/open")
        assert response.status_code == 200
        assert "Dispenser opened successfully" in response.json["message"]

        response = client.get(f"api/dispenser/{dispenser.id}")
        assert response.status_code == 200
        data = response.json
        assert "id" in data
        assert "flow_volume" in data
        assert "price" in data
        assert "is_open" in data

        assert data["id"] == dispenser.id
        assert data["flow_volume"] == 0.5
        assert data["price"] == 2.0
        assert data["is_open"] == True

    def test_non_existing_dispenser_id(self, test_setup):
        client, _, _ = test_setup

        response = client.get("/api/dispenser/9999")
        assert response.status_code == 404
        assert "Dispenser not found" in response.json["message"]

    def test_get_all_dispensers(self, test_setup):
        client, db, _ = test_setup

        dispenser1 = Dispenser(flow_volume=0.5, price=2.0)
        dispenser2 = Dispenser(flow_volume=0.3, price=1.5)
        db.session.add_all([dispenser1, dispenser2])
        db.session.commit()

        response = client.get("api/dispenser")
        assert response.status_code == 200
        data = response.json
        assert isinstance(data, list)
        assert len(data) == 2

        assert data[0]["flow_volume"] == 0.5
        assert data[0]["price"] == 2.0

        assert data[1]["flow_volume"] == 0.3
        assert data[1]["price"] == 1.5

    def test_open_dispenser(self, test_setup):
        client, db, _ = test_setup
        dispenser = Dispenser(flow_volume=0.5, price=2.0)
        db.session.add(dispenser)
        db.session.commit()

        response = client.post(f"api/dispenser/{dispenser.id}/open")
        assert response.status_code == 200
        assert "Dispenser opened successfully" in response.json["message"]

        updated_dispenser = db.session.get(Dispenser, dispenser.id)
        assert updated_dispenser.is_open is True

    def test_open_already_open_dispenser(self, test_setup):
        client, db, _ = test_setup

        dispenser = Dispenser(flow_volume=0.5, price=2.0)
        db.session.add(dispenser)
        dispenser.is_open = True
        db.session.commit()

        response = client.post(f"api/dispenser/{dispenser.id}/open")
        assert response.status_code == 400
        assert "Dispenser is already open" in response.json["message"]

    def test_close_dispenser(self, test_setup):
        client, db, _ = test_setup

        dispenser = Dispenser(flow_volume=0.5, price=2.0)
        db.session.add(dispenser)
        db.session.flush()  # Required to populate dispenser.id without commiting
        transaction = Transaction(dispenser.id, datetime.now())
        db.session.add(transaction)
        dispenser.is_open = True
        db.session.commit()

        response = client.post(f"api/dispenser/{dispenser.id}/close")
        assert response.status_code == 200

        updated_dispenser = db.session.get(Dispenser, dispenser.id)
        assert updated_dispenser.is_open is False

    def test_close_already_closed_dispenser(self, test_setup):
        client, db, _ = test_setup

        dispenser = Dispenser(flow_volume=0.5, price=2.0)
        db.session.add(dispenser)
        db.session.commit()

        response = client.post(f"api/dispenser/{dispenser.id}/close")
        assert response.status_code == 400
        assert "Dispenser is already closed" in response.json["message"]
