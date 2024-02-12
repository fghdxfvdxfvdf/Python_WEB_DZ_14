from pathlib import Path
import unittest
BASE_DIR = Path(__file__).resolve().parent.parent
import sys
sys.path.append(str(BASE_DIR))

from fastapi.testclient import TestClient
from main import app  



client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200


if __name__ == '__main__':
    unittest.main()
