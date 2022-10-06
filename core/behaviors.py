from core import models


class BaixaNoEstoqueBehavior:
    def __init__(self, sale: models.Sale):
        self.sale = sale

    def _get_stock_address_entry(self):
        pass

    def _get_stock_address_exit(self):
        pass

    def _generate_movment_stock(self):
        for item in self.sale.saleitem_set.all():
            # item.quantity
            pass

    def run(self):
        self._get_stock_address_entry()
        self._get_stock_address_exit()
        self._generate_movment_stock()
