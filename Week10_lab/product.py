from abc import ABC, abstractmethod

from supplier import Supplier


class Product(ABC):
    def __init__(
        self,
        product_id: str,
        name: str,
        price: float,
        stock: int,
        supplier: Supplier
    ) -> None:
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier

    @property
    def price(self) -> float:
        return self.__price

    @property
    def supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> None:
        self.__stock = quantity

    def display_information(self) -> None:
        print(f"ID: {self.__product_id}")
        print(f"Name: {self.__name}")
        print(f"Price: ${self.__price:.2f}")
        print(f"Stock: {self.__stock}")

    def display_supplier_information(self) -> None:
        self.__supplier.display_information()

    def get_product_id(self) -> str:
        return self.__product_id


    def to_dict(self) -> dict:
        return {
            "id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
            "supplier": self.__supplier.to_dict()
        }


    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass
