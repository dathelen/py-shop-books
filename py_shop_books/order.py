class ShopifyOrder(object):
    def __init__(self, id):
       self.__id = id 
       self.__items = []
       self.__customer  = None
    @property
    def items(self):
       return self.__items
    @property
    def customer(self):
       return self.__customer
    @customer.setter
    def items(self, value):
       self.__customer = value
    def add_item(self, value):
       self.__item.append(value)
