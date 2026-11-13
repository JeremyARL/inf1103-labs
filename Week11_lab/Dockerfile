FROM python:3.12-slim

WORKDIR /app

COPY *.py ./
COPY inventory.json products.csv ./
COPY tests/ ./tests/

RUN python -m pip install --no-cache-dir pytest

CMD ["python", "inventory_manager.py"]
