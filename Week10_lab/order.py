from product import Product
from order_line import OrderLine


class Order:
    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def add_order_line(
        self, product: Product, quantity: int
    ) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for order_line in self.__order_lines:
            if order_line.product.get_product_id() == product_id:
                self.__order_lines.remove(order_line)
                return True

        return False

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

    def calculate_total(self) -> float:
        total = 0.0

        for order_line in self.__order_lines:
            total += order_line.calculate_subtotal()

        return total

    def display_information(self) -> None:
        print(f"Order ID: {self.__order_id}")

        for order_line in self.__order_lines:
            print(
                f"Product ID: {order_line.product.get_product_id()}, "
                f"Quantity: {order_line.quantity}, "
                f"Subtotal: ${order_line.calculate_subtotal():.2f}"
            )

        print(f"Order Total: ${self.calculate_total():.2f}")
