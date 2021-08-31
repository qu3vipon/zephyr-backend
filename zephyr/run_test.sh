alembic upgrade head
python -m pytest --cov="." --cov-report term:skip-covered
echo "==================================== FLAKE ===================================="
python -m flake8 ./zephyr/app
echo "==================================== BLACK ===================================="
python -m black ./zephyr/app
echo "==================================== ISORT ===================================="
python -m isort ./zephyr/app