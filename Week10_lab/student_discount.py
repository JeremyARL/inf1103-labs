from discount_strategy import DiscountStrategy


class StudentDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.95