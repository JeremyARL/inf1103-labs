class Supplier:
    def __init__(
        self,
        supplier_id: str,
        name: str,
        contact_email: str
    ) -> None:
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.__supplier_id}")
        print(f"Supplier Name: {self.__name}")
        print(f"Contact Email: {self.__contact_email}")

    def to_dict(self) -> dict[str, str]:
        return {
            "supplier_id": self.__supplier_id,
            "name": self.__name,
            "contact_email": self.__contact_email
        }
