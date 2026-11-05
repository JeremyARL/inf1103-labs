FROM python:3.12-slim

WORKDIR /app

COPY product.py physical_product.py digital_product.py can_be_shipped.py inventory.py inventory_manager.py supplier.py order.py order_line.py inventory.json ./

COPY tests/ ./tests/

CMD ["python", "inventory_manager.py"]
