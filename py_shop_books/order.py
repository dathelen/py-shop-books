class ShopifyOrder(object):
    def __init__(self, id):
       self.__id = id 
       self.__items = []
       self.__customer  = None
       self.__customer_id = None
    @property
    def items(self):
        return self.__items

    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self, value):
        self.__id = value


    @property
    def customer(self):
        return self.__customer
    @customer.setter
    def customer(self, value):
        self.__customer = value
    @property
    def customer_id(self):
        return self.__customer_id
    @customer_id.setter
    def customer_id(self, value):
        self.__customer_id = value


    def add_item(self, value):
        self.__items.append(value)

    def total_cost(self):
        cost  = 0
        for item in self.__items:
            cost += item.total_price()
        return cost
            
