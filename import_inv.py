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
V = 2
def read_shop_export(transactions):
    pass
    
def find_customer_id(order, client):
    customers = []
    customer_id = None
    #first need to find customer in quicken
    if V > 2:
        print('trying to find customers for order {}'.format(order.id))
    if order.customer['Billing Company'] != '':
        try:
            search = order.customer['Billing Company'].split()[0]
        except IndexError:
            search = order.customer['Billing Company']
        customers = Customer.where("Active = True and CompanyName LIKE '%{}%'".format(search), 
                                  qb=client)
        if len(customers) == 0:
            if V > 2:
                print("Did not find a match for {} in Billing Company".format(search))
        else:
            if V > 2:
                print(f'found {len(customers)} that matched {search}')
                print("Order #{} is for customer: {}".format(order.id, str(customers[0])))
            customer_id = customers[0].Id


    if order.customer['Billing Name']!= '' and len(customers) == 0:
        try:
            last_name = order.customer['Billing Name'].split()[1]
        except IndexError:
            last_name = order.customer['Billing Name']

        customers = Customer.where("Active = True and FamilyName LIKE '%{}%'".format(last_name), 
                                  qb=client)
        if len(customers) == 0:
            if V > 2:
                print("Did not find a match for {}".format(order.customer['Billing Name']))
        else:
            if V > 2:
                print(f'found {len(customers)} that matched {last_name}')
                print("Order #{} is for customer: {}".format(order.id, str(customers[0])))
            customer_id = customers[0].Id

    if order.customer['Email'] != '' and len(customers) == 0:
        email = order.customer['Email'].split('@')[1].split('.')[0]
        if V > 2:
            print(f'email is {email}')
        if email == 'gmail':
            email = order.customer['Email']
        customers = Customer.where("Active = True and PrimaryEmailAddr LIKE '%{}%'".format(email),
                          qb=client)
        if len(customers) == 0:
            if V > 2:
                print("Did not find a match for {}".format(order.customer['Email']))
        else:
            if V > 2:
                print(f'found {len(customers)} that matched {email}')
                print("Order #{} is for customer: {}".format(order.id, str(customers[0])))
            customer_id = customers[0].Id
    if len(customers) > 0 and V > 1:
        print(f'Order {order.id} is for customer {str(customers[0])}')
    return customer_id

def parse_customer_info(row):
    to_return = {}
    to_return['Billing Company'] = row['Billing Company']
    to_return['Billing Name'] = row['Billing Name']
    to_return['Email'] = row['Email']

    return to_return

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
       print('You need a new refresh token.  Run the server in the SampleOauth2_UsingPythonClient: python manage.py runserer if you are in the sandbox.  If you are in Prod you need ot get one from the Developer Dashboard Redirect')
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
        v.customer_id = find_customer_id(v, client)
        if v.customer_id is None:
            print(f'No customer found for order {k}')
            
   

if __name__ == "__main__":
    main()
