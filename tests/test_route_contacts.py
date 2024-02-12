from pathlib import Path
import unittest
BASE_DIR = Path(__file__).resolve().parent.parent

import sys
sys.path.append(str(BASE_DIR))

from unittest.mock import MagicMock, patch, AsyncMock
from datetime import date

import pytest

from src.database.models import User
from src.services.auth import auth_service

CONTACT = {
    'first_name': 'Max',
    'last_name': 'Greb',
    'email': 'Max_Greb@example.com',
    'phone_number': '+38098123789',
    'birth_date': date.today(),
    'additional_data': 'string'
}

@pytest.fixture()
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)

    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    response = client.post("/api/auth/login", data={"username": user.get("email"), "password": user.get("password")})
    data = response.json()
    return data["access_token"]


from unittest.mock import patch
from datetime import date


def test_create_contact(client, token):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        contact = client.post("/api/contacts", json={"email": "user@example.com"},
                              headers={"Authorization": f"Bearer {token}"})
        data = contact.json()
        contact_id = data.get("id")

        CONTACT["birth_date"] = date.today().isoformat()

        CONTACT["contact_id"] = contact_id
        response = client.post("/api/contacts",
                               json=CONTACT,
                               headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data



def test_get_contacts(client, token, monkeypatch):
    with patch.object(auth_service, "r") as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.redis', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.identifier', AsyncMock())
        monkeypatch.setattr('fastapi_limiter.FastAPILimiter.http_callback', AsyncMock())
        response = client.get("/api/contacts",
                              headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200, response.text
        data = response.json()
        assert type(data) == list
        assert data[0]["first_name"] == CONTACT["first_name"]
        