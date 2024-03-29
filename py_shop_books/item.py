class ShopifyItem(object):
    def __init__(self, *args, **kwargs):
        self.__name = kwargs['name']
        self.__quantity = int(kwargs['quantity'])
        self.__unit_price = float(kwargs['unit_price'])
        self.__qb_item = None

    @property
    def name(self):
       return self.__name
    @name.setter
    def name(self, value):
       self.__name = value

    @property
    def quantity(self):
       return self.__quantity
    @quantity.setter
    def quantity(self):
       self.__quantity = int(value)

    @property
    def unit_price(self):
       return self.__unit_price

    @unit_price.setter
    def unit_price(self, value):
       self.__unit_price = int(value)

    @property
    def qb_item(self):
       return self.__qb_item

    @qb_item.setter
    def qb_item(self, value):
       self.__qb_item = value


    def total_price(self):
       return self.__quantity * self.__unit_price


