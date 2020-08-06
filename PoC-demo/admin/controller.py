### Admins setup flow
from bitcoinrpc.authproxy import AuthServiceProxy
import requests

node = AuthServiceProxy('http://user:password@0.0.0.0:38232')

def new_z_address():
    addr = node.z_getnewaddress()
    return addr

def create_new_product(_name, _addr, _period, _scope, _price):
    return requests.post('http://127.0.0.1:8000/api/create_product', data={
        'name': _name,
        'address': _addr,
        'period': _period,
        'scope': _scope,
        'price': _price
    })

def main():
    print(create_new_product(
        'Product1',
        new_z_address(),
        86000,
        'premium',
        100000000
    ))

main()
