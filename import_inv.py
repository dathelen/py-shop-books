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
    
def parse_customer_info(row):
    # shopify doesn't enforce exactly where customer info goes so we get to guess
    # Its in 1 of 3 locations, in order of preference:
    # 1. Billing Customer
    # 2. Billing Name
    # 3. Try Guess from Email
    key = None
    value = None
    if row['Billing Customer'] != '' 
        key = 'Billing Customer'
    elif row['Billing Name'] != ''
        key = 'Billing Name'
    elif row['Email'] != ''
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
            print('current row is {}'.format(id))
            new_item = ShopifyItem(name=row['Lineitem name'], quanity=row['Lineitem quantity'],
                                   unit_price = row['Lineitem price'])

            if last_row == id:
               print('Same Transaction')
               orders[row['Name'].replace('#', '')].add_item(new_item)
            else:
               print('New Transaction')
               order = ShopifyOrder(name=row['Name']) 
               order.customer = parse_customer_info(row)
               order.add_item(new_item)

               orders[row['Name'].replace('#', '')] = order

            last_row = id



   


if __name__ == "__main__":
    main()
