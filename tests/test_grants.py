import pytest
from datetime import datetime, timedelta, UTC
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

VALID_PAYLOAD = {
    'document_id': 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
    'grantee_id': '22222222-2222-2222-2222-222222222222',
    'created_by': '11111111-1111-1111-1111-111111111111',
    'permission': 'view',
    'expires_at': (datetime.now(UTC) + timedelta(minutes=10)).isoformat()
}


def test_create_grant_success():
    response = client.post('/grants', json=VALID_PAYLOAD)
    assert response.status_code in [200, 201, 409]


def test_expiry_validation():
    payload = VALID_PAYLOAD.copy()
    payload['grantee_id'] = str(uuid4())
    payload['expires_at'] = (datetime.now(UTC) + timedelta(seconds=20)).isoformat()

    response = client.post('/grants', json=payload)
    assert response.status_code == 400


def test_duplicate_active_grant():
    response1 = client.post('/grants', json=VALID_PAYLOAD)
    response2 = client.post('/grants', json=VALID_PAYLOAD)
    assert response2.status_code == 409


def test_list_grants():
    response = client.get('/grants')
    assert response.status_code == 200

