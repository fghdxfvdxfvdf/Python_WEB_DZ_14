docker-compose up
docker-compose up -d
docker run --name hw_13-postgres -p 5432:5432 -e POSTGRES_PASSWORD=567234 -e POSTGRES_DB=hw_13 -d postgres


alembic init migrations
alembic revision --autogenerate -m 'Init'
alembic upgrade head



uvicorn main:app --reload
python -m uvicorn main:app --host localhost --port 8000 --reload


http://localhost:8000/docs


poetry add --dev $(cat requirements.txt)

poetry add sphinx -G dev
sphinx-quickstart docs
    docs\conf.py і docs\index.rst   модифікувати

cd docs 
.\make.bat html

http://127.0.0.1:5500/docs/_build/html/index.html


pytest tests

pytest tests\test_route_contacts.py
pytest tests\conftest.py
pytest tests\test_main.py
pytest tests\test_route_auth.py
pytest tests\test_unit_repository_contacts.py

pytest --help
