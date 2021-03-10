import csv
import pandas as pd
import yaml
import json
from py_shop_books.client import connect
from py_shop_books.order import ShopifyOrder
from py_shop_books.item import ShopifyItem
from intuitlib.exceptions import AuthClientError
from quickbooks.objects.customer import Customer


CFG_FILE = '/home/dt/.pyshopcfg.yaml'
ENV = 'PRODUCTION'

def read_shop_export(transactions):
    pass
    
def create_invoice(order, client):
   #first need to find customer in quicken
    if order.customer['key'] == 'Billing Company':
       # search on subet of company entry
       search = order.customer['value'].split()[0]
       if search == 'The':
         search = 'Chapel'
       customers = Customer.where("Active = True and CompanyName LIKE '%{}%'".format(search), 
                                  qb=client)
       if len(customers) == 0:
           print("Did not find a match for {}".format(search))
       else:
           print("Order #{} is for customer: {}".format(order.id, str(customers[0])))
           order.customer_id = customers[0].Id
    elif order.customer['key'] == 'Billing Name':
        try:
            last_name = order.customer['value'].split()[1]
        except IndexError:
            last_name = order.customer['value']

        customers = Customer.where("Active = True and FamilyName LIKE '%{}%'".format(last_name), 
                                  qb=client)
        if len(customers) == 0:
            print("Did not find a match for {}".format(order.customer['value']))
        else:
            print("Order #{} is for customer: {}".format(order.id, str(customers[0])))
            order.customer_id = customers[0].Id

def parse_customer_info(row):
    # shopify doesn't enforce exactly where customer info goes so we get to guess
    # Its in 1 of 3 locations, in order of preference:
    # 1. Billing Customer
    # 2. Billing Name
    # 3. Try Guess from Email
    key = None
    value = None
    if row['Billing Company'] != '': 
        key = 'Billing Company'
    elif row['Billing Name'] != '':
        key = 'Billing Name'
    elif row['Email'] != '':
        key = 'Email'

    if key is not None:
        value = row[key]

    return {'key': key, 'value': value}

def main():
    # read in config file
    with open(CFG_FILE, 'r') as cfg:
       client_config = yaml.full_load(cfg)
    print(client_config)

    #get a client
    try:
        client = connect(client_config[ENV]['CLIENT_ID'],
                         client_config[ENV]['CLIENT_SECRET'],
                         client_config[ENV]['REFRESH_TOKEN'],
                         client_config[ENV]['REDIRECT_URI'],
                         client_config[ENV]['COMPANY_ID'],
                         environment=ENV.lower())
    except AuthClientError:
       print('You need a new refresh token.  Run the server in the SampleOauth2_UsingPythonClient: python manage.py runserer')
       exit(-1)
        
    orders = {}

    with open('orders_export_1.csv', newline='') as data:
        transactions = csv.DictReader(data, delimiter=',')
        last_row = None
        for row in transactions:
            id = row['Name']
            new_item = ShopifyItem(name=row['Lineitem name'], quantity=row['Lineitem quantity'],
                                   unit_price = row['Lineitem price'])

            if last_row == id:
               orders[row['Name'].replace('#', '')].add_item(new_item)
            else:
               print('New Transaction: {}'.format(row['Name']))
               order = ShopifyOrder(id=row['Name']) 
               order.customer = parse_customer_info(row)
               order.add_item(new_item)

               orders[row['Name'].replace('#', '')] = order

            last_row = id
    print("total orders is {}".format(len(orders.keys())))
    for k,v in orders.items():
        create_invoice(v, client)



   


if __name__ == "__main__":
    main()
