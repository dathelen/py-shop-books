import yaml
from py_shop_books.client import connect

CFG_FILE = '/home/dt/.pyshopcfg.yaml'
ENV = 'SANDBOX'

def main():
    # read in config file
    with open(CFG_FILE, 'r') as cfg:
       client_config = yaml.full_load(cfg)
    print(client_config)

    #get a client
    client = connect(client_config[ENV]['CLIENT_ID'],
                     client_config[ENV]['CLIENT_SECRET'],
                     client_config[ENV]['REFRESH_TOKEN'],
                     client_config[ENV]['REDIRECT_URI'],
                     client_config[ENV]['COMPANY_ID'])


if __name__ == "__main__":
    main()
