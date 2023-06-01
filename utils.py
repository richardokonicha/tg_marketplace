from config import *
from models import *


class DbClient:
    "Performing CRUD functions and access to the Database"

    def get_user_by_id(self, id: string) -> User | None:
        "Get user"
        pass

    def get_products(self) -> list:
        "return list of products available"
        pass

    def get_product_by_id(self, id: int) -> Product | None:
        "Returns a single product item"
        pass

    def get_orders(self, user_id) -> list:
        "Fetch orders by user_id"
        pass

    def get_order_by_id(self, id: int) -> Order | None:
        "Fetch a single order by id"
        pass


db_client = DbClient()
